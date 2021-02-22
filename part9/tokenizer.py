#!/usr/bin/env python
from collections import namedtuple
"""
Context-free grammar

program                 : compound_statement DOT
compound_statement      : BEGIN statement_list END
statement_list          : statement
                        | statement SEMI statement_list
statement               : compound_statement
                        | assignment_statement
                        | empty
assignment_statement    : variable ASSIGN expr
variable                : ID
empty                   :
expr                    : term ((PLUS | MINUS) term) *
term                    : factor ((TIMES | DIVIDE) factor) *
factor                  : PLUS factor
                        | MINUS factor
                        | INTEGER
                        | LPAREN expr RPAREN
                        | variable
"""


"""
Tokens
"""
Token = namedtuple('Token', ('type', 'value'))

class Tokenizer:
    end_of_file = Token('EOF', None)
    keywords = {
        'BEGIN': Token('BEGIN', 'BEGIN'),
        'END': Token('END', 'END'),
        ':=': Token('ASSIGN', ':='),
    }
    operations = {
        '+': Token('PLUS', '+'),
        '-': Token('MINUS', '-'),
        '*': Token('TIMES', '*'),
        '/': Token('DIVIDE', '/'),
    }

    def __init__(self, program):
        self.program = program
        self.index = 0
        self.current_char = self.program[self.index] if self.program else ''

    def get_next_char(self):
        self.index += 1
        try:
            self.current_char = self.program[self.index]
        except IndexError:
            self.current_char = ''
        return self.current_char

    def peak(self):
        try:
            return self.program[self.index + 1]
        except IndexError:
            return ''

    def next_is_number(self):
        return (
            self.current_char.isdigit() or
            (self.current_char == '.' and self.peak().isdigit())
        )

    def integer(self):
        result = self.current_char
        while self.get_next_char().isdigit():
            result += self.current_char
        return result

    def number(self):
        first_part = self.integer() if self.current_char.isdigit() else ''

        if self.current_char == '.' and self.get_next_char().isdigit():
            second_part = self.integer()
        else:
            second_part = ''

        if first_part and second_part:
            result = '{}.{}'.format(first_part, second_part)
        elif first_part:
            result = first_part
        else:
            result = '.{}'.format(second_part)

        return Token('Number', result)

    def operation(self):
        result = self.operations[self.current_char]
        self.get_next_char()
        return result

    def get_next_token(self):
        while self.current_char and self.current_char.isspace():
            self.get_next_char()

        if self.current_char in self.operations:
            result = self.operation()
        elif self.next_is_number():
            result = self.number()
        else:
            result = self.end_of_file

        return result

    def tokenize(self):
        while (next_token := self.get_next_token()) != self.end_of_file:
            yield next_token



if __name__ == '__main__':
    while (in_str := input('9>')) != 'exit':
        tokenizer = Tokenizer(in_str)
        for token in tokenizer.tokenize():
            print(token)
        tokens = list(tokenizer.tokenize())
        print(tokens)
        print(' '.join(t.value for t in tokens))
