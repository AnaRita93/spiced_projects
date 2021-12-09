"""
Automated Testing

    pip install pytest
"""
NUMBERS = '12345678'

def count_words(text):
    for digit in NUMBERS:
        text = text.replace(digit, '')
    words = text.split()
    return  len(words)
    