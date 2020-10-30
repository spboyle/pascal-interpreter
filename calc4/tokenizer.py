#!/usr/bin/env python

from collections import namedtuple
import operator

Token = namedtuple('Token', ('value', 'type'))

PLUS, MINUS, TIMES, DIVIDE = 'PLUS', 'MINUS', 'TIMES', 'DIVIDE'
INTEGER = 'INTEGER'
LPAREN, RPAREN = 'LPAREN', 'RPAREN'
EOF = 'EOF'


operations = {
    '+': lambda: Token('+', PLUS),
    '-': lambda: Token('-', MINUS),
    '*': lambda: Token('*', TIMES),
    '/': lambda: Token('/', DIVIDE),
    '(': lambda: Token('(', LPAREN),
    ')': lambda: Token(')', RPAREN),
}


def advance(text, index):
    """
    Returns the index of the next non-whitespace character and that character
    len(text), '' if reached the end
    """
    index += 1
    char = ''
    while index < len(text) and not (char := text[index].strip()):
        index += 1

    if index > len(text):
        return len(text), ''

    return index, char


def tokenize(text):
    index, char = advance(text, -1)

    while index < len(text):
        if char in operations:
            token = operations[char]()
            index, char = advance(text, index)
            yield token
        elif char.isdigit():
            number = char
            index += 1
            while index < len(text) and (char := text[index].strip()).isdigit():
                number += char
                index += 1
            yield Token(int(number), INTEGER)
            if not char.strip():
                index, char = advance(text, index)
        else:
            raise Exception('Unrecognized character: "{}"'.format(char))



if __name__ == '__main__':
    while not (text := input('tokenizer> ')).startswith('exit'):
        try:
            for token in tokenize(text):
                print(token)
        except Exception as e:
            print(e)
