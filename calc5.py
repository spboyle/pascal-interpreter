#!/usr/bin/env python

from collections import namedtuple
import traceback


Token = namedtuple('Token', ('type', 'value'))

PLUS, MINUS, TIMES, DIVIDE, NUMBER, EOF, LPAREN, RPAREN = (
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'NUMBER', 'EOF', 'LPAREN', 'RPAREN'
)

operations = {
    '+': Token(PLUS, '+'),
    '-': Token(MINUS, '-'),
    '*': Token(TIMES, '*'),
    '/': Token(DIVIDE, '/'),
    '(': Token(LPAREN, '('),
    ')': Token(RPAREN, ')'),
}


class Node:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


class Scanner:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def advance(self):
        self.pos += 1
        if self.pos < len(self.text):
            self.current_char = self.text[self.pos]
        else:
            self.current_char = ''

    def integer(self):
        result = self.current_char
        self.advance()
        decimal_point_found = result == '.'
        while self.current_char.isdigit() or (not decimal_point_found and self.current_char == '.'):
            result += self.current_char
            if self.current_char == '.':
                decimal_point_found = True
            self.advance()

        return Token(NUMBER, float(result))

    def get_next_token(self):
        while self.current_char.isspace():
            self.advance()

        if self.current_char == '':
            return Token(EOF, None)
        if self.current_char.isdigit() or self.current_char == '.':
            return self.integer()
        elif self.current_char in operations:
            result = operations[self.current_char]
            self.advance()
            return result
        else:
            raise Exception('Unsanctioned character: {}'.format(self.current_char))


class Parser:
    def __init__(self, scanner):
        self.scanner = scanner
        self.current_token = self.scanner.get_next_token()

    def eat(self, type):
        if type == self.current_token.type:
            self.current_token = self.scanner.get_next_token()
        else:
            raise Exception('Mismatched token types: Expected {}, got {}'.format(type, self.current_token.type))

    def expr(self):
        result = self.term()

        while self.current_token.type in [PLUS, MINUS]:
            if self.current_token.type == PLUS:
                self.eat(PLUS)
                result = Node('+', result, self.term())
            else:
                self.eat(MINUS)
                result = Node('-', result, self.term())

        return result

    def term(self):
        result = self.factor()

        while self.current_token.type in [TIMES, DIVIDE]:
            if self.current_token.type == TIMES:
                self.eat(TIMES)
                result = Node('*', result, self.factor())
            else:
                self.eat(DIVIDE)
                result = Node('/', result, self.factor())

        return result

    def factor(self):
        if self.current_token.type == NUMBER:
            result = Node(self.current_token.value)
            self.eat(NUMBER)
        elif self.current_token.type == LPAREN:
            self.eat(LPAREN)
            result = self.expr()
            self.eat(RPAREN)
        else:
            raise Exception('Expected NUMBER or LPAREN, got {}'.format(self.current_token.type))
        return result


class Interpreter:
    operations = {
        '+': lambda x, y: x + y,
        '-': lambda x, y: x - y,
        '*': lambda x, y: x * y,
        '/': lambda x, y: x / y,
    }
    def __init__(self, ast):
        self.ast = ast

    def evaluate(self):
        return self.crunch_tree(self.ast)

    def crunch_tree(self, node):
        if node.value in self.operations:
            return self.operations[node.value](self.crunch_tree(node.left), self.crunch_tree(node.right))
        else:
            return node.value


class Postfixer:
    """
    Converts math AST into postfix
    """
    operations = ('+', '*', '-', '/')

    def __init__(self, ast):
        self.ast = ast

    def evaluate(self):
        return self.to_postfix(self.ast)

    def to_postfix(self, node):
        if node.value in self.operations:
            string = "{} {} {}".format(self.to_postfix(node.left), self.to_postfix(node.right), node.value)
        elif node.value.is_integer():
            string = str(int(node.value))
        else:
            string = str(node.value)

        return string


class Lisper:
    """
    Converts math AST into prefix but includes parens to mimic lisp
    """
    operations = ('+', '*', '-', '/')

    def __init__(self, ast):
        self.ast = ast

    def evaluate(self):
        return self.to_lisp(self.ast)

    def to_lisp(self, node):
        if node.value in self.operations:
            string = "({} {} {})".format(node.value, self.to_lisp(node.left), self.to_lisp(node.right))
        elif node.value.is_integer():
            string = str(int(node.value))
        else:
            string = str(node.value)

        return string


if __name__ == '__main__':
    while not (text:= input('calc5> ')).startswith('exit'):
        try:
            # tokens = []
            # scanner = Scanner(text)
            # while (token := scanner.get_next_token()).type != EOF:
            #     tokens.append(token.value)
            # print(tokens)
            parser = Parser(Scanner(text))
            tree = parser.expr()

            interpreter = Interpreter(tree)
            print(interpreter.evaluate())

        except Exception as e:
            traceback.print_exc()
