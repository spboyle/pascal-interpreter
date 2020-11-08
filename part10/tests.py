#!/usr/bin/env python
import unittest

from lexer import Lexer
from interpreter import Interpreter
from parser import Parser


class TestLexer(unittest.TestCase):
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
        self.assertEqual(['begin', 'end'], tokens)

    def test_program_with_statements(self):
        string = 'BEGIN a := 5; x := 11 END'
        lexer = Lexer(string)
        tokens = [token.value for token in lexer.tokenize()]
        self.assertEqual(['begin', 'a', ':=', '5', ';', 'x', ':=', '11', 'end'], tokens)

    def test_program_with_comments(self):
        """
        Ignores all characters in {comments}
        """
        string = 'BEGIN a := 5; {hi ∞} x := 11 END'
        lexer = Lexer(string)
        tokens = [token.value for token in lexer.tokenize()]
        self.assertEqual(['begin', 'a', ':=', '5', ';', 'x', ':=', '11', 'end'], tokens)


class TestInterpreter(unittest.TestCase):

    def test_mixed_expr_1(self):
        """
        5 - 2 * 6 + 8 ==> 1
        """
        text = '5 - 2 * 6 + 8'
        interpreter = Interpreter(Parser(Lexer(text).tokenize()).parse())
        self.assertEqual(interpreter.interpret(), 1)

    def test_mixed_expr_2(self):
        """
        5 + 2 - 3 * 3 ==> -2
        """
        text = '5 + 2 - 3 * 3'
        interpreter = Interpreter(Parser(Lexer(text).tokenize()).parse())
        self.assertEqual(interpreter.interpret(), -2)

    def test_mixed_expr_3(self):
        """
        6 - 8*3 + 19 div 5 + 85 div 17 - 3*4 ==> -21.2
        """
        text = '6 - 8*3 + 19/5 + 85 div 17 - 3*4'
        interpreter = Interpreter(Parser(Lexer(text).tokenize()).parse())
        self.assertEqual(interpreter.interpret(), -21.2)

    def test_repeated_minus(self):
        """
        9 - 5 - 3 - 12 ==> -11
        """
        text = '9 - 5 - 3 - 12'
        interpreter = Interpreter(Parser(Lexer(text).tokenize()).parse())
        self.assertEqual(interpreter.interpret(), -11)

    def test_repeated_divide(self):
        """
        3600 div 12 div 3 div 25 ==> 4
        """
        text = '3600 div 12 div 3 div 25'
        interpreter = Interpreter(Parser(Lexer(text).tokenize()).parse())
        self.assertEqual(interpreter.interpret(), 4)

    def test_mixed_multiply_divide(self):
        """
        3600 div 12 * 3 div 25 * 2 / 100 ==> .72
        """
        text = '3600 div 12 * 3 div 25 * 2 / 100'
        interpreter = Interpreter(Parser(Lexer(text).tokenize()).parse())
        self.assertEqual(interpreter.interpret(), .72)

    def test_mixed_addition_subtraction(self):
        """
        36 - 12 + 3 - 25 + 2 - 10  ==> -6
        """
        text = '36 - 12 + 3 - 25 + 2 - 10'
        interpreter = Interpreter(Parser(Lexer(text).tokenize()).parse())
        self.assertEqual(interpreter.interpret(), -6)

    def test_parens(self):
        """
        36 - (12 + 3) - (25 + 2) div 9  ==> 18
        """
        text = '36 - (12 + 3) - (25 + 2) div 9'
        parser = Parser(Lexer(text).tokenize())
        interpreter = Interpreter(parser.parse())
        self.assertEqual(interpreter.interpret(), 18)

    def test_parens_2(self):
        """
        7 + 3 * (10 div (12 div (3 + 1) - 1))  ==> 22
        """
        text = '7 + 3 * (10 div (12 div (3 + 1) - 1))'
        parser = Parser(Lexer(text).tokenize())
        interpreter = Interpreter(parser.parse())
        self.assertEqual(interpreter.interpret(), 22)

    def test_unary_1(self):
        """
        - 3 =>  -3
        """
        text = '- 3'
        parser = Parser(Lexer(text).tokenize())
        interpreter = Interpreter(parser.parse())
        self.assertEqual(interpreter.interpret(), -3)

    def test_unary_2(self):
        """
        + 3 =>  3
        """
        text = '+ 3'
        parser = Parser(Lexer(text).tokenize())
        interpreter = Interpreter(parser.parse())
        self.assertEqual(interpreter.interpret(), 3)

    def test_unary_3(self):
        """
        5 - - - + - 3 =>  8
        """
        text = '5 - - - + - 3'
        parser = Parser(Lexer(text).tokenize())
        interpreter = Interpreter(parser.parse())
        self.assertEqual(interpreter.interpret(), 8)

    def test_unary_4(self):
        """
        5 - - - + - (3 + 4) - +2 =>  10
        """
        text = '5 - - - + - (3 + 4) - +2'
        parser = Parser(Lexer(text).tokenize())
        interpreter = Interpreter(parser.parse())
        self.assertEqual(interpreter.interpret(), 10)

    def test_program_with_statements(self):
        text = 'BEGIN a := 5; x := 11 END.'
        parser = Parser(Lexer(text).tokenize())
        interpreter = Interpreter(parser.parse_program())
        self.assertEqual({'a': 5, 'x': 11}, interpreter.interpret())

    def test_program_with_var_manipulation(self):
        text = """
        BEGIN
            BEGIN
                number := 2;
                a := number;
                b := 10 * a + 10 * number div 4;
                c := a - - b
            END;
            x := 11;
        END.
        """
        parser = Parser(Lexer(text).tokenize())
        interpreter = Interpreter(parser.parse_program())
        self.assertEqual({'number': 2, 'a': 2, 'b': 25, 'c': 27, 'x': 11}, interpreter.interpret())

    def test_program_case_insensitive(self):
        text = """
        Begin
            BeGiN
                NUMBER := 2;
                A := nuMBer;
                b := 10 * a + 10 * NUmbEr div 4;
                c := a - - B
            end;
            x := 11;
        END.
        """
        parser = Parser(Lexer(text).tokenize())
        interpreter = Interpreter(parser.parse_program())
        self.assertEqual({'number': 2, 'a': 2, 'b': 25, 'c': 27, 'x': 11}, interpreter.interpret())

    def test_program_underscores_in_var_names(self):
        text = """
        Begin
            BeGiN
                _NUMBER := 2;
                A := _nuMBer;
                b_b := 10 * a + 10 * _NUmbEr div 4;
                c := a - - B_b
            end;
            x := 11;
        END.
        """
        parser = Parser(Lexer(text).tokenize())
        interpreter = Interpreter(parser.parse_program())
        self.assertEqual({'_number': 2, 'a': 2, 'b_b': 25, 'c': 27, 'x': 11}, interpreter.interpret())


if __name__ == '__main__':
    unittest.main()
