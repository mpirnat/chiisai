"""Core shortener logic"""

from hashlib import md5


def make_hash(value):
    """Make a url-friendly md5 hash of a value."""
    md_5 = md5()
    md_5.update(value)

    # get the hashed value, being careful to strip out characters
    # that are not url-safe
    hashed = md_5.digest().encode('base64')\
            .replace('\n','')\
            .rstrip('=')\
            .replace('/', '')\
            .replace('+', '')

    return hashed


bad_words = ['fuck', 'shit', 'piss', 'cock', 'cunt', 'tits', 'bitch']

def is_clean(value):
    """Is the value devoid of 'unsavory' language?"""
    value = value.lower()
    for bad_word in bad_words:
        if bad_word in value:
            return False
    return True
