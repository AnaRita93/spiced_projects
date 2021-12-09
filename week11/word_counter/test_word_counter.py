"""
Automated Testing

    pip install pytest
"""
from word_counter import count_words
import pytest

def test_empty():
    assert count_words('') == 0 

def test_hello():
    assert count_words('hello') == 1

def test_hello_world():
    assert count_words('hello world') == 2

def test_phone():
    assert count_words('my phone number is 12345678') == 4 

def test_number_in_word():
    assert count_words('Neo4J is cool') == 3

def tests_fails_with_invalid_data():
    with pytest.raises(Exception):
        assert count_words(9999)
