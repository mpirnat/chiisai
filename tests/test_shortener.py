"""Tests for the shortener component"""

from nose.tools import assert_equals
from chiisai import shortener


class TestWhenMakingHash(object):

    def setup(self):
        self.url = 'http://example.com'
        self.hashed = shortener.make_hash(self.url)

    def test_it_makes_a_hash(self):
        expected_hash = 'qbnwQzbOAYGgjndOARE7MQ'
        assert_equals(self.hashed, expected_hash)
