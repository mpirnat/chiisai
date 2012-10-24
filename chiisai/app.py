from contextlib import closing
from flask import Flask, g, request, session, \
        abort, redirect, render_template, url_for

from chiisai import forms
from chiisai import storage
from chiisai import shortener


app = Flask(__name__)
app.config.from_object('chiisai.settings')
app.config.from_envvar('CHIISAI_SETTINGS', silent=True)


@app.before_request
def before_request():
    """Make sure we are connected to the database each request."""
    g.db = storage.connect_db(app)


@app.teardown_request
def teardown_request(exception):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'db'):
        g.db.close()


@app.route('/')
def index():
    return 'Hello, world!'


@app.route('/admin/new', methods=['GET'])
def new_short_url_form():
    """Provide a human-friendly form for shortening URLs."""
    return render_template('new_url.html')


@app.route('/admin/new', methods=['POST'])
def create_short_url():
    """Provide a POSTable, human-friendly interface for shortening URLs."""
    short_url = _create_short_url(request.form)
    return short_url


@app.route('/api/new', methods=['GET', 'POST'])
def create_short_url_api():
    """
    Provide an GET/POSTable interface that can be connected to clients that
    support custom shorteners (eg, Tweetbot).
    """
    short_url = _create_short_url(request.form or request.args)
    return short_url


def _create_short_url(form_data):
    form = forms.URLShortenerForm(form_data)
    if not form.validate():
        # TODO: error gracefully
        abort(400)

    url = form.url.data
    alias = form.alias.data or None
    explicit_alias_requested = alias is not None

    try:
        alias = shortener.make_alias(url, alias=alias)
    except shortener.UncleanAlias:
        # TODO: error gracefully
        abort(400)

    try:
        shortener.insert_url(url, alias, g.db)
    except storage.NotUnique:
        # That alias is already claimed; you can't have it
        if explicit_alias_requested:
            long_url = shortener.get_url(alias, g.db)
            if url != long_url:
                # TODO: error gracefully
                abort(403)

        # Hashed to the same thing?  Be idempotent
        else:
            pass

    short_url = url_for('short_url', alias=alias, _external=True)
    return short_url


@app.route('/<alias>', methods=['GET'])
def short_url(alias):
    """Look up and redirect to a long URL."""
    try:
        url = shortener.get_url(alias, g.db)
    except storage.NotFound:
        abort(404)
    return redirect(url, code=301)


if __name__ == '__main__':
    app.run()
