#!/usr/bin/env python

from collections import namedtuple
import operator
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


class Lexer:

    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def advance(self):
        self.pos += 1
        try:
            self.current_char = self.text[self.pos]
        except IndexError:
            self.current_char = ''

    def number(self):
        result = self.current_char
        self.advance()
        decimal_found = self.current_char == '.'
        while self.current_char.isdigit() or (not decimal_found and self.current_char == '.'):
            if self.current_char == '.':
                decimal_found = True
            result += self.current_char
            self.advance()

        try:
            return Token(NUMBER, int(result))
        except ValueError:
            return Token(NUMBER, float(result))


    def tokenize(self):
        while self.current_char:
            if self.current_char.isspace():
                self.advance()
                continue

            elif self.current_char.isdigit() or self.current_char == '.':
                yield self.number()
                # self.number() already advances to the next non-digit char
            elif self.current_char in operations:
                yield operations[self.current_char]
                self.advance()
            else:
                raise ValueError('Invalid character: {}'.format(self.current_char))


class Node:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right
        self.is_op = self.value in operations


class Parser:
    """
    expr : term ((PLUS|MINUS)term)*
    term : factor ((TIMES|DIVIDE)factor)*
    factor : INTEGER | LPAREN expr RPAREN
    """

    def __init__(self, tokens):
        self.tokens = tokens
        self.get_next_token()

    def get_next_token(self):
        self.current_token = next(self.tokens, Token(EOF, None))

    def eat(self, type):
        if type == self.current_token.type:
            self.get_next_token()
        else:
            raise TypeError('Expected token {}, got {}'.format(type, self.current_token.type))

    def parse(self):
        return self.expr()

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
            raise TypeError('Expected NUMBER or LPAREN, got {}'.format(self.current_token.type))

        return result




class Interpreter:
    operations = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '/': operator.truediv,
    }

    def __init__(self, ast):
        self.ast = ast

    def interpret(self):
        return self.crunch(self.ast)

    def crunch(self, node):
        if node.value in operations:
            return self.operations[node.value](self.crunch(node.left), self.crunch(node.right))
        else:
            return node.value


if __name__ == '__main__':
    while not (text := input('calc6> ')).startswith('exit'):
        try:
            tokens = list(Lexer(text).tokenize())
            print(tokens)
            parser = Parser(iter(tokens))
            interpreter = Interpreter(parser.parse())
            print(interpreter.interpret())
        except:
            traceback.print_exc()
