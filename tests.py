#!/usr/bin/env python
import unittest

from calc1 import Interpreter


class TestInterpreter(unittest.TestCase):

    def test_mixed_expr_1(self):
        """
        5 - 2 * 6 + 8 ==> 1
        """
        text = '5 - 2 * 6 + 8'
        interpreter = Interpreter(text)
        self.assertEqual(interpreter.expr(), 1)

    def test_mixed_expr_2(self):
        """
        5 + 2 - 3 * 3 ==> -2
        """
        text = '5 + 2 - 3 * 3'
        interpreter = Interpreter(text)
        self.assertEqual(interpreter.expr(), -2)

    def test_mixed_expr_3(self):
        """
        6 - 8*3 + 19/5 + 85 / 17 - 3*4 ==> -21.2
        """
        text = '6 - 8*3 + 19/5 + 85 / 17 - 3*4'
        interpreter = Interpreter(text)
        self.assertEqual(interpreter.expr(), -21.2)

    def test_repeated_minus(self):
        """
        9 - 5 - 3 - 12 ==> -11
        """
        text = '9 - 5 - 3 - 12'
        interpreter = Interpreter(text)
        self.assertEqual(interpreter.expr(), -11)

    def test_repeated_divide(self):
        """
        3600 / 12 / 3 / 25 ==> 4
        """
        text = '3600 / 12 / 3 / 25'
        interpreter = Interpreter(text)
        self.assertEqual(interpreter.expr(), 4)

    def test_mixed_multiply_divide(self):
        """
        3600 / 12 * 3 / 25 * 2 / 100 ==> .72
        """
        text = '3600 / 12 * 3 / 25 * 2 / 100'
        interpreter = Interpreter(text)
        self.assertEqual(interpreter.expr(), .72)

    def test_mixed_addition_subtraction(self):
        """
        36 - 12 + 3 - 25 + 2 - 10  ==> -6
        """
        text = '36 - 12 + 3 - 25 + 2 - 10'
        interpreter = Interpreter(text)
        self.assertEqual(interpreter.expr(), -6)


if __name__ == '__main__':
    unittest.main()
