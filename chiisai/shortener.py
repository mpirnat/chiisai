"""Core shortener logic"""

import datetime
from hashlib import md5
from chiisai import base
from chiisai import storage


class UncleanAlias(ValueError):
    pass


ALIAS_LENGTH = 4
def make_alias(url, alias=None, length=ALIAS_LENGTH):
    if alias and not is_clean(alias):
        raise UncleanAlias("alias '{0}' is not clean".format(alias))

    attempt = 0
    attempt_url = url

    while not alias:
        hashed = make_hash(attempt_url)

        if is_clean(hashed):
            alias = hashed[:length]

        else:
            attempt += 1
            attempt_url = "{url}#{attempt}".format(**locals())

    return alias


def make_hash(value):
    """Make a url-friendly md5 hash of a value."""
    md_5 = md5()
    md_5.update(value)

    # get the hashed value, being careful to strip out characters
    # that are not url-safe
    hashed = base.base_encode(
            base.bytestring_to_integer(
                md_5.digest()))

    return hashed


reserved_words = ('admin',)
bad_words = ['fuck', 'shit', 'piss', 'cock', 'cunt', 'tits', 'bitch']

def is_clean(value):
    """Is the value devoid of 'unsavory' language?"""
    value = value.lower()

    if value.startswith(reserved_words):
        return False

    for word in reserved_words:
        if word in value:
            return False

    for word in bad_words:
        if word in value:
            return False

    return True


def insert_url(url, alias, db):
    sql = "insert into urls(alias, url, created, hits) "\
            "values(?, ?, ?, 0)"
    created = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.000")
    storage.query_db(sql, [alias, url, created], db=db)
    db.commit()


def get_url(alias, db):
    sql = "select url from urls where alias = ?"
    result = storage.query_db(sql, [alias], one=True, db=db)
    if not result:
        raise storage.NotFound()
    return result['url']


def record_hit(alias, db):
    sql = "update urls set hits = hits + 1 where alias = ?"
    storage.query_db(sql, [alias], db=db)
    db.commit()
