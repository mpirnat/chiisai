"""Shortener stuff"""

from hashlib import md5


def make_hash(value):
    md_5 = md5()
    md_5.update(value)
    hashed = md_5.digest().encode('base64').replace('\n','').rstrip('=')
    return hashed
