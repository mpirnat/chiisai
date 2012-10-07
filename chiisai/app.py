from contextlib import closing
from flask import Flask, g, request, session, \
        abort, redirect, render_template, url_for

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
    return render_template('new_url.html')


@app.route('/admin/new', methods=['POST'])
def create_short_url():

    url = request.form['url']

    alias = request.form['alias'] or None
    try:
        alias = shortener.make_alias(url, alias=alias)
    except shortener.UncleanAlias:
        abort(400)

    try:
        shortener.insert_url(url, alias, g.db)
    except storage.NotUnique:
        # Alias not unique? That's okay, we're totally idempotent!
        pass

    short_url = url_for('short_url', alias=alias, _external=True)
    return short_url


@app.route('/<alias>', methods=['GET'])
def short_url(alias):
    try:
        url = shortener.get_url(alias, g.db)
    except storage.NotFound:
        abort(404)
    return redirect(url, code=301)


if __name__ == '__main__':
    app.run()
