#!/usr/bin/env python
import unittest

from calc6 import Parser, Lexer
from calc6 import Interpreter as Interpreter6


class TestInterpreter6(unittest.TestCase):

    def test_mixed_expr_1(self):
        """
        5 - 2 * 6 + 8 ==> 1
        """
        text = '5 - 2 * 6 + 8'
        interpreter = Interpreter6(Parser(Lexer(text).tokenize()).parse())
        self.assertEqual(interpreter.interpret(), 1)

    def test_mixed_expr_2(self):
        """
        5 + 2 - 3 * 3 ==> -2
        """
        text = '5 + 2 - 3 * 3'
        interpreter = Interpreter6(Parser(Lexer(text).tokenize()).parse())
        self.assertEqual(interpreter.interpret(), -2)

    def test_mixed_expr_3(self):
        """
        6 - 8*3 + 19/5 + 85 / 17 - 3*4 ==> -21.2
        """
        text = '6 - 8*3 + 19/5 + 85 / 17 - 3*4'
        interpreter = Interpreter6(Parser(Lexer(text).tokenize()).parse())
        self.assertEqual(interpreter.interpret(), -21.2)

    def test_repeated_minus(self):
        """
        9 - 5 - 3 - 12 ==> -11
        """
        text = '9 - 5 - 3 - 12'
        interpreter = Interpreter6(Parser(Lexer(text).tokenize()).parse())
        self.assertEqual(interpreter.interpret(), -11)

    def test_repeated_divide(self):
        """
        3600 / 12 / 3 / 25 ==> 4
        """
        text = '3600 / 12 / 3 / 25'
        interpreter = Interpreter6(Parser(Lexer(text).tokenize()).parse())
        self.assertEqual(interpreter.interpret(), 4)

    def test_mixed_multiply_divide(self):
        """
        3600 / 12 * 3 / 25 * 2 / 100 ==> .72
        """
        text = '3600 / 12 * 3 / 25 * 2 / 100'
        interpreter = Interpreter6(Parser(Lexer(text).tokenize()).parse())
        self.assertEqual(interpreter.interpret(), .72)

    def test_mixed_addition_subtraction(self):
        """
        36 - 12 + 3 - 25 + 2 - 10  ==> -6
        """
        text = '36 - 12 + 3 - 25 + 2 - 10'
        interpreter = Interpreter6(Parser(Lexer(text).tokenize()).parse())
        self.assertEqual(interpreter.interpret(), -6)

    def test_parens(self):
        """
        36 - (12 + 3) - (25 + 2) / 9  ==> 18
        """
        text = '36 - (12 + 3) - (25 + 2) / 9'
        parser = Parser(Lexer(text).tokenize())
        interpreter = Interpreter6(parser.parse())
        self.assertEqual(interpreter.interpret(), 18)

    def test_parens_2(self):
        """
        7 + 3 * (10 / (12 / (3 + 1) - 1))  ==> 22
        """
        text = '7 + 3 * (10 / (12 / (3 + 1) - 1))'
        parser = Parser(Lexer(text).tokenize())
        interpreter = Interpreter6(parser.parse())
        self.assertEqual(interpreter.interpret(), 22)

    def test_unary_1(self):
        """
        - 3 =>  -3
        """
        text = '- 3'
        parser = Parser(Lexer(text).tokenize())
        interpreter = Interpreter6(parser.parse())
        self.assertEqual(interpreter.interpret(), -3)


    def test_unary_2(self):
        """
        + 3 =>  3
        """
        text = '+ 3'
        parser = Parser(Lexer(text).tokenize())
        interpreter = Interpreter6(parser.parse())
        self.assertEqual(interpreter.interpret(), 3)


    def test_unary_3(self):
        """
        5 - - - + - 3 =>  8
        """
        text = '5 - - - + - 3'
        parser = Parser(Lexer(text).tokenize())
        interpreter = Interpreter6(parser.parse())
        self.assertEqual(interpreter.interpret(), 8)


    def test_unary_4(self):
        """
        5 - - - + - (3 + 4) - +2 =>  10
        """
        text = '5 - - - + - (3 + 4) - +2'
        parser = Parser(Lexer(text).tokenize())
        interpreter = Interpreter6(parser.parse())
        self.assertEqual(interpreter.interpret(), 10)

    # def test_to_postfix(self):
    #     """
    #     7 + 3 * (10 / (12 / (3 + 1) - 1)) => 7 3 10 12 3 1 + / 1 - / * +'
    #     """
    #     text = '7 + 3 * (10 / (12 / (3 + 1) - 1))'
                        #     postfixer = Postfixer(Parser(Lexer(text).tokenize()).expr())
    #     self.assertEqual(postfixer.evaluate(), '7 3 10 12 3 1 + / 1 - / * +')

    # def test_to_postfix_2(self):
    #     """
    #     (5 + 3) * 12 / 3 => 5 3 + 12 * 3 /
    #     """
    #     text = '(5 + 3) * 12 / 3'
                        #     postfixer = Postfixer(Parser(Lexer(text).tokenize()).expr())
    #     self.assertEqual(postfixer.evaluate(), '5 3 + 12 * 3 /')

    # def test_to_lisp(self):
    #     """
    #     2 + 3 => (+ 2 3)
    #     """
    #     text = '2 + 3'
                        #     lisper = Lisper(Parser(Lexer(text).tokenize()).expr())
    #     self.assertEqual(lisper.evaluate(), '(+ 2 3)')

    # def test_to_lisp_2(self):
    #     """
    #     2 + 3 * 5 => (+ 2 (* 3 5))
    #     """
    #     text = '2 + 3 * 5'
                        #     lisper = Lisper(Parser(Lexer(text).tokenize()).expr())
    #     self.assertEqual(lisper.evaluate(), '(+ 2 (* 3 5))')

    # def test_to_lisp_3(self):
    #     """
    #     (5 + 3) * 12 / 3 => 5 3 + 12 * 3 /
    #     """
    #     text = '(5 + 3) * 12 / 3'
                        #     lisper = Lisper(Parser(Lexer(text).tokenize()).expr())
    #     self.assertEqual(lisper.evaluate(), '(/ (* (+ 5 3) 12) 3)')


if __name__ == '__main__':
    unittest.main()
