#!/usr/bin/env python
import unittest

from calc1 import Interpreter as Interpreter1
from calc2 import Interpreter as Interpreter2
from calc5 import Interpreter as Interpreter5
from calc5 import Parser, Scanner, Postfixer, Lisper


class TestInterpreter1(unittest.TestCase):

    def test_mixed_expr_1(self):
        """
        5 - 2 * 6 + 8 ==> 1
        """
        text = '5 - 2 * 6 + 8'
        interpreter = Interpreter1(text)
        self.assertEqual(interpreter.expr(), 1)

    def test_mixed_expr_2(self):
        """
        5 + 2 - 3 * 3 ==> -2
        """
        text = '5 + 2 - 3 * 3'
        interpreter = Interpreter1(text)
        self.assertEqual(interpreter.expr(), -2)

    def test_mixed_expr_3(self):
        """
        6 - 8*3 + 19/5 + 85 / 17 - 3*4 ==> -21.2
        """
        text = '6 - 8*3 + 19/5 + 85 / 17 - 3*4'
        interpreter = Interpreter1(text)
        self.assertEqual(interpreter.expr(), -21.2)

    def test_repeated_minus(self):
        """
        9 - 5 - 3 - 12 ==> -11
        """
        text = '9 - 5 - 3 - 12'
        interpreter = Interpreter1(text)
        self.assertEqual(interpreter.expr(), -11)

    def test_repeated_divide(self):
        """
        3600 / 12 / 3 / 25 ==> 4
        """
        text = '3600 / 12 / 3 / 25'
        interpreter = Interpreter1(text)
        self.assertEqual(interpreter.expr(), 4)

    def test_mixed_multiply_divide(self):
        """
        3600 / 12 * 3 / 25 * 2 / 100 ==> .72
        """
        text = '3600 / 12 * 3 / 25 * 2 / 100'
        interpreter = Interpreter1(text)
        self.assertEqual(interpreter.expr(), .72)

    def test_mixed_addition_subtraction(self):
        """
        36 - 12 + 3 - 25 + 2 - 10  ==> -6
        """
        text = '36 - 12 + 3 - 25 + 2 - 10'
        interpreter = Interpreter1(text)
        self.assertEqual(interpreter.expr(), -6)


class TestInterpreter2(unittest.TestCase):
    def test_mixed_expr_1(self):
        """
        5 - 2 * 6 + 8 ==> 1
        """
        text = '5 - 2 * 6 + 8'
        interpreter = Interpreter2(text)
        self.assertEqual(interpreter.expr(), 1)

    def test_mixed_expr_2(self):
        """
        5 + 2 - 3 * 3 ==> -2
        """
        text = '5 + 2 - 3 * 3'
        interpreter = Interpreter2(text)
        self.assertEqual(interpreter.expr(), -2)

    def test_mixed_expr_3(self):
        """
        6 - 8*3 + 19/5 + 85 / 17 - 3*4 ==> -21.2
        """
        text = '6 - 8*3 + 19/5 + 85 / 17 - 3*4'
        interpreter = Interpreter2(text)
        self.assertEqual(interpreter.expr(), -21.2)

    def test_repeated_minus(self):
        """
        9 - 5 - 3 - 12 ==> -11
        """
        text = '9 - 5 - 3 - 12'
        interpreter = Interpreter2(text)
        self.assertEqual(interpreter.expr(), -11)

    def test_repeated_divide(self):
        """
        3600 / 12 / 3 / 25 ==> 4
        """
        text = '3600 / 12 / 3 / 25'
        interpreter = Interpreter2(text)
        self.assertEqual(interpreter.expr(), 4)

    def test_mixed_multiply_divide(self):
        """
        3600 / 12 * 3 / 25 * 2 / 100 ==> .72
        """
        text = '3600 / 12 * 3 / 25 * 2 / 100'
        interpreter = Interpreter2(text)
        self.assertEqual(interpreter.expr(), .72)

    def test_mixed_addition_subtraction(self):
        """
        36 - 12 + 3 - 25 + 2 - 10  ==> -6
        """
        text = '36 - 12 + 3 - 25 + 2 - 10'
        interpreter = Interpreter2(text)
        self.assertEqual(interpreter.expr(), -6)


class TestCalc5(unittest.TestCase):

    def test_mixed_expr_1(self):
        """
        5 - 2 * 6 + 8 ==> 1
        """
        text = '5 - 2 * 6 + 8'
        parser = Parser(Scanner(text))
        interpreter = Interpreter5(parser.expr())
        self.assertEqual(interpreter.evaluate(), 1)

    def test_mixed_expr_2(self):
        """
        5 + 2 - 3 * 3 ==> -2
        """
        text = '5 + 2 - 3 * 3'
        parser = Parser(Scanner(text))
        interpreter = Interpreter5(parser.expr())
        self.assertEqual(interpreter.evaluate(), -2)

    def test_mixed_expr_3(self):
        """
        6 - 8*3 + 19/5 + 85 / 17 - 3*4 ==> -21.2
        """
        text = '6 - 8*3 + 19/5 + 85 / 17 - 3*4'
        parser = Parser(Scanner(text))
        interpreter = Interpreter5(parser.expr())
        self.assertEqual(interpreter.evaluate(), -21.2)

    def test_repeated_minus(self):
        """
        9 - 5 - 3 - 12 ==> -11
        """
        text = '9 - 5 - 3 - 12'
        parser = Parser(Scanner(text))
        interpreter = Interpreter5(parser.expr())
        self.assertEqual(interpreter.evaluate(), -11)

    def test_repeated_divide(self):
        """
        3600 / 12 / 3 / 25 ==> 4
        """
        text = '3600 / 12 / 3 / 25'
        parser = Parser(Scanner(text))
        interpreter = Interpreter5(parser.expr())
        self.assertEqual(interpreter.evaluate(), 4)

    def test_mixed_multiply_divide(self):
        """
        3600 / 12 * 3 / 25 * 2 / 100 ==> .72
        """
        text = '3600 / 12 * 3 / 25 * 2 / 100'
        parser = Parser(Scanner(text))
        interpreter = Interpreter5(parser.expr())
        self.assertEqual(interpreter.evaluate(), .72)

    def test_mixed_addition_subtraction(self):
        """
        36 - 12 + 3 - 25 + 2 - 10  ==> -6
        """
        text = '36 - 12 + 3 - 25 + 2 - 10'
        parser = Parser(Scanner(text))
        interpreter = Interpreter5(parser.expr())
        self.assertEqual(interpreter.evaluate(), -6)

    def test_parens(self):
        """
        36 - (12 + 3) - (25 + 2) / 9  ==> 18
        """
        text = '36 - (12 + 3) - (25 + 2) / 9'
        parser = Parser(Scanner(text))
        interpreter = Interpreter5(parser.expr())
        self.assertEqual(interpreter.evaluate(), 18)

    def test_parens_2(self):
        """
        7 + 3 * (10 / (12 / (3 + 1) - 1))  ==> 22
        """
        text = '7 + 3 * (10 / (12 / (3 + 1) - 1))'
        parser = Parser(Scanner(text))
        interpreter = Interpreter5(parser.expr())
        self.assertEqual(interpreter.evaluate(), 22)

    def test_to_postfix(self):
        """
        7 + 3 * (10 / (12 / (3 + 1) - 1)) => 7 3 10 12 3 1 + / 1 - / * +'
        """
        text = '7 + 3 * (10 / (12 / (3 + 1) - 1))'
        postfixer = Postfixer(Parser(Scanner(text)).expr())
        self.assertEqual(postfixer.evaluate(), '7 3 10 12 3 1 + / 1 - / * +')

    def test_to_postfix_2(self):
        """
        (5 + 3) * 12 / 3 => 5 3 + 12 * 3 /
        """
        text = '(5 + 3) * 12 / 3'
        postfixer = Postfixer(Parser(Scanner(text)).expr())
        self.assertEqual(postfixer.evaluate(), '5 3 + 12 * 3 /')

    def test_to_lisp(self):
        """
        2 + 3 => (+ 2 3)
        """
        text = '2 + 3'
        lisper = Lisper(Parser(Scanner(text)).expr())
        self.assertEqual(lisper.evaluate(), '(+ 2 3)')

    def test_to_lisp_2(self):
        """
        2 + 3 * 5 => (+ 2 (* 3 5))
        """
        text = '2 + 3 * 5'
        lisper = Lisper(Parser(Scanner(text)).expr())
        self.assertEqual(lisper.evaluate(), '(+ 2 (* 3 5))')

    def test_to_lisp_3(self):
        """
        (5 + 3) * 12 / 3 => 5 3 + 12 * 3 /
        """
        text = '(5 + 3) * 12 / 3'
        lisper = Lisper(Parser(Scanner(text)).expr())
        self.assertEqual(lisper.evaluate(), '(/ (* (+ 5 3) 12) 3)')

if __name__ == '__main__':
    unittest.main()
