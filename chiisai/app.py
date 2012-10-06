from contextlib import closing
from flask import Flask, g
from sqlite3 import dbapi2 as sqlite3


app = Flask(__name__)
app.config.from_object('chiisai.settings')
app.config.from_envvar('CHIISAI_SETTINGS', silent=True)


def connect_db():
    """Returns a new connection to the database."""
    return sqlite3.connect(app.config['DATABASE'])


def init_db():
    """Creates the database tables."""
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql') as f:
            db.cursor().executescript(f.read())
        db.commit()


def query_db(query, args=(), one=False):
    """Makes querying the database a little nicer."""
    cursor = g.db.execute(query, args)
    result = [dict((cursor.description[i][0], value)
                for i, value in enumerate(row))
                for row in cursor.fetchall()]
    return (result[0] if result else None) if one else result


@app.before_request
def before_request():
    """Make sure we are connected to the database each request."""
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'db'):
        g.db.close()


@app.route('/')
def index():
    return 'Hello, world!'


if __name__ == '__main__':
    app.run()
