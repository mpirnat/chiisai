"""Shortener stuff"""

from hashlib import md5


def make_hash(value):
    md_5 = md5()
    md_5.update(value)
    hashed = md_5.digest().encode('base64')\
            .replace('\n','')\
            .rstrip('=')\
            .replace('/', '')\
            .replace('+', '')
    return hashed


bad_words = ['fuck', 'shit', 'piss', 'cock', 'bitch', 'cunt']

def is_clean(value):
    value = value.lower()
    for bad_word in bad_words:
        if bad_word in value:
            return False
    return True
