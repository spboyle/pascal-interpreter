#!/usr/bin/env python

from collections import namedtuple
import string

from constants import (
    PLUS, MINUS, TIMES, DIVIDE, INTEGER_DIVIDE, LPAREN, RPAREN,
    NUMBER, VARIABLE, ASSIGN,
    SEMICOLON, BEGIN, END, DOT, DIV, EOF,
)

Token = namedtuple('Token', ('type', 'value'))

"""
Lexical Analysis
"""
class Lexer:
    operations = {
        '+': Token(PLUS, '+'),
        '-': Token(MINUS, '-'),
        '*': Token(TIMES, '*'),
        '/': Token(DIVIDE, '/'),
        '(': Token(LPAREN, '('),
        ')': Token(RPAREN, ')'),
    }
    end_of_file = Token(EOF, None)
    assignment_token = Token(ASSIGN, ':=')
    semicolon = Token(SEMICOLON, ';')
    dot = Token(DOT, '.')

    reserved_words = {
        BEGIN: Token(BEGIN, BEGIN),
        END: Token(END, END),
        DIV: Token(INTEGER_DIVIDE, DIV)
    }

    acceptable_var_starters = string.ascii_letters + '_'
    acceptable_var_chars = acceptable_var_starters + string.digits

    def __init__(self, text):
        self.text = text
        self.reset()

    def reset(self):
        self.pos = 0
        self.current_char = self.text[self.pos]

    def advance(self):
        self.pos += 1
        try:
            self.current_char = self.text[self.pos]
        except IndexError:
            self.current_char = ''

    def peek(self):
        try:
            return self.text[self.pos + 1]
        except IndexError:
            return ''

    def _id(self):
        result = ''
        if self.current_char in self.acceptable_var_starters:
            while self.current_char and self.current_char in self.acceptable_var_chars:
                result += self.current_char
                self.advance()
        return result

    def identifier(self):
        identifier = self._id().lower()
        if identifier:
            return self.reserved_words.get(identifier, Token(VARIABLE, identifier))

    def assignment(self):
        if self.current_char == ':':
            self.advance()
            if self.current_char == '=':
                token = ':='
                self.advance()
                return token

    def number(self):
        result = ''
        decimal_found = self.current_char == '.'
        while self.current_char.isdigit() or (not decimal_found and self.current_char == '.'):
            result += self.current_char
            self.advance()

        return Token(NUMBER, result) if result else None

    def get_next_token(self):
        while self.current_char:
            # Skip spaces
            if self.current_char.isspace():
                self.advance()

            # Skip comments
            elif self.current_char == '{':
                while self.current_char and self.current_char != '}':
                    self.advance()
                self.advance()

            # End of statement
            elif self.current_char == ';':
                self.advance()
                return self.semicolon
            # End of program
            elif self.current_char == '.':
                self.advance()
                return self.dot

            # multi-char tokens which advance self.current_char
            elif (identifier := self.identifier()):
                return identifier
            elif (number := self.number()):
                return number
            elif (assignment := self.assignment()):
                return self.assignment_token

            # Single-char operations like + - * /
            elif self.current_char in self.operations:
                token = self.operations[self.current_char]
                self.advance()
                return token
            else:
                raise ValueError(f'Unexpected character {self.current_char}')

        # End of file
        return self.end_of_file

    def tokenize(self):
        self.reset()
        while (token := self.get_next_token()).type != EOF:
            yield token
