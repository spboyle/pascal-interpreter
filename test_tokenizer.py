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


if __name__ == '__main__':
    unittest.main()
