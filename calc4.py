#!/usr/bin/env python

import traceback

from calc4.tokenizer import (
    tokenize,
    PLUS,
    MINUS,
    TIMES,
    DIVIDE,
    EOF,
    INTEGER,
    LPAREN,
    RPAREN
)


class Parser:
    """
    expr : term((PLUS|MINUS)term)*
    term : factor((MUL|DIV)factor)*
    factor : INTEGER | LPAREN expr RPAREN
    """


    def __init__(self, tokens):
        """
        tokens is an iterable of a tokenized statement
        """
        self.tokens = tokens
        self.current_token = next(self.tokens, None)

    def expr(self):
        result = self.term()

        while self.current_token and self.current_token.type in [PLUS, MINUS]:
            if self.current_token.type == PLUS:
                self.eat(PLUS)
                result += self.term()
            else:
                self.eat(MINUS)
                result -= self.term()

        return result

    def term(self):
        result = self.factor()

        while self.current_token and self.current_token.type in [TIMES, DIVIDE]:
            if self.current_token.type == TIMES:
                self.eat(TIMES)
                result *= self.factor()
            else:
                self.eat(DIVIDE)
                result /= self.factor()

        return result

    def factor(self):
        if self.current_token.type == INTEGER:
            result = self.current_token.value
            self.eat(INTEGER)
        elif self.current_token.type == LPAREN:
            self.eat(LPAREN)
            result = self.expr()
            self.eat(RPAREN)

        return result

    def eat(self, type):
        if type == self.current_token.type:
            self.current_token = next(self.tokens, None)
        else:
            raise Exception('Expected {}, got {}'.format(type, self.current_token.type))

    def evaluate(self):
        return self.expr()


if __name__ == '__main__':
    while not (text := input('calc4> ')).startswith('exit'):
        try:
            tokens = list(tokenize(text))
            print(tokens)
            parser = Parser(iter(tokens))
            print(parser.evaluate())
        except Exception as e:
            traceback.print_exc()
