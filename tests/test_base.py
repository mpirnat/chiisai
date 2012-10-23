"""Tests for base conversion."""

from chiisai.base import base_encode, base_decode
from chiisai.base import bytestring_to_integer, integer_to_bytestring


def check_case(f, input_, expected):
    actual = f(input_)
    assert actual == expected, actual


base62_cases = [
        (0, '0'),
        (1, '1'),
        (10, 'A'),
        (35, 'Z'),
        (36, 'a'),
        (61, 'z'),
        (62, '10'),
        (3844, '100'),
        (238328, '1000'),
        (14776336, '10000'),
        (916132832, '100000'),
        (56800235584, '1000000'),
]

def test_converting_base10_to_base62():

    for integer, expected in base62_cases:
        yield check_case, base_encode, integer, expected


def test_converting_base62_to_base10():

    for expected, encoded in base62_cases:
        yield check_case, base_decode, encoded, expected


bytestring_cases = [
    ('\x00', 0),
    ('\x01', 1),
    ('\xff', 255),
    ('\x00\x01', 256),
    ('\x01\x01', 257),
    ('\xff\x01', 511),
    ('\x00\x02', 512),
    ('\xff\x02', 767),
    ('\x00\x03', 768),
    ('\xff\xff', 65535),
    ('\x00\x00\x01', 65536),
]

def test_converting_bytestrings_to_integers():

    for bytestring, expected in bytestring_cases:
        yield check_case, bytestring_to_integer, bytestring, expected


def test_converting_integers_to_bytestrings():

    for expected, integer in bytestring_cases:
        yield check_case, integer_to_bytestring, integer, expected
