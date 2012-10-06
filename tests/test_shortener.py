"""Tests for the shortener component"""

from nose.tools import assert_equals
from chiisai import shortener


class TestWhenMakingHash(object):

    def test_it_makes_a_hash(self):
        value = 'http://example.com'
        expected_hash = 'qbnwQzbOAYGgjndOARE7MQ'

        hashed = shortener.make_hash(value)

        assert_equals(hashed, expected_hash)

    def test_it_makes_a_urlsafe_hash(self):
        value = 'foobaristan'

        hashed = shortener.make_hash(value)

        assert '+' not in hashed, hashed
        assert '/' not in hashed, hashed

        assert '?' not in hashed, hashed
        assert '#' not in hashed, hashed
        assert '=' not in hashed, hashed
        assert '&' not in hashed, hashed


class TestCensoringHash(object):

    def test_it_passes_innocuous_strings(self):
        hashed = 'puppies and rainbows'
        assert shortener.is_clean(hashed)

    def test_it_fails_censorable_strings(self):
        hashed = 'fuck12qDSffagwa467MQagaRE7'
        assert not shortener.is_clean(hashed)

    def test_it_finds_mixed_case_bad_words(self):
        hashed = 'fUcK12qDSffagwa467MQagaRE7'
        assert not shortener.is_clean(hashed)

