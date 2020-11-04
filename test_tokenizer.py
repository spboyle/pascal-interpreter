#!/usr/bin/env python

import unittest

from calc9 import Lexer


class LexerTestCase(unittest.TestCase):
    def test_basic_addition(self):
        string = "2+3"
        lexer = Lexer(string)
        tokens = [token.value for token in lexer.tokenize()]
        self.assertEqual(['2', '+', '3'], tokens)

    def test_surrounding_space(self):
        string = ' 2 + 3 '
        lexer = Lexer(string)
        tokens = [token.value for token in lexer.tokenize()]
        self.assertEqual(['2', '+', '3'], tokens)

    def test_all_chars(self):
        string = ' 2.9 + (3 - 4) * 5 / 10 '
        lexer = Lexer(string)
        tokens = [token.value for token in lexer.tokenize()]
        self.assertEqual(['2.9', '+', '(', '3', '-', '4', ')', '*', '5', '/', '10'], tokens)

    def test_var(self):
        string = 'a'
        lexer = Lexer(string)
        tokens = [token.value for token in lexer.tokenize()]
        self.assertEqual(['a'], tokens)

    def test_assignment_and_variable(self):
        string = 'a := 4'
        lexer = Lexer(string)
        tokens = [token.value for token in lexer.tokenize()]
        self.assertEqual(['a', ':=', '4'], tokens)

    def test_assignment_and_variable_with_semicolon(self):
        string = 'a := 4'
        lexer = Lexer(string)
        tokens = [token.value for token in lexer.tokenize()]
        self.assertEqual(['a', ':=', '4'], tokens)

    def test_empty_program(self):
        string = 'BEGIN END'
        lexer = Lexer(string)
        tokens = [token.value for token in lexer.tokenize()]
        self.assertEqual(['BEGIN', 'END'], tokens)

    def test_program_with_statements(self):
        string = 'BEGIN a := 5; x := 11 END'
        lexer = Lexer(string)
        tokens = [token.value for token in lexer.tokenize()]
        self.assertEqual(['BEGIN', 'a', ':=', '5', ';', 'x', ':=', '11', 'END'], tokens)


if __name__ == '__main__':
    unittest.main()
