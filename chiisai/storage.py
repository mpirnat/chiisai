from flask import g
from sqlite3 import dbapi2 as sqlite3

class NotFound(Exception):
    pass


class NotUnique(Exception):
    pass


def connect_db(app):
    """Returns a new connection to the database."""
    return sqlite3.connect(app.config['DATABASE'])


def init_db(app):
    """Creates the database tables."""
    with closing(connect_db(app)) as db:
        with app.open_resource('schema.sql') as f:
            db.cursor().executescript(f.read())
        db.commit()


def query_db(query, args=(), one=False, db=None):
    """Makes querying the database a little nicer."""
    db = db or g.db
    try:
        cursor = db.execute(query, args)
    except sqlite3.IntegrityError, e:
        if "not unique" in str(e):
            raise NotUnique()
        raise

    result = [dict((cursor.description[i][0], value)
                for i, value in enumerate(row))
                for row in cursor.fetchall()]
    return (result[0] if result else None) if one else result
