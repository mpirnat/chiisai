"""Tests for base conversion."""

from chiisai.base import base_encode, base_decode


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

    def check_case(base10, base62):
        assert base_encode(base10) == base62

    for base10, base62 in base62_cases:
        yield check_case, base10, base62


def test_converting_base62_to_base10():

    def check_case(base62, base10):
        assert base_decode(base62) == base10

    for base10, base62 in base62_cases:
        yield check_case, base62, base10
