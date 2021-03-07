#!/usr/bin/env python

import logging

from ast import (
    BinaryOp, UnaryOp, NoOp,
    Number, Assignment, Variable,
    Compound
)
from constants import (
    PLUS, MINUS, TIMES, DIVIDE, INTEGER_DIVIDE, LPAREN, RPAREN,
    NUMBER, VARIABLE, ASSIGN,
    SEMICOLON, BEGIN, END, DOT, DIV
)
from lexer import Lexer

"""
Syntax Analysis

program                 : PROGRAM variable SEMI block DOT
block                   : declarations compound_statement
declarations            : VAR (variable_declaration SEMI)+ | empty
variable_declaration    : variable (COMMA variable)* COLON variable_type
variable_type           : INTEGER | REAL
compound_statement      : BEGIN statement_list END
statement_list          : statement
                        | statement SEMI statement_list
statement               : compound_statement
                        | assignment_statement
                        | empty
assignment_statment     : variable ASSIGN expr
variable                : ID
expr                    : term ((PLUS|MINUS)term)*
term                    : factor ((TIMES|DIVIDE)factor)*
factor                  : (PLUS|MINUS)factor
                        |  NUMBER
                        | LPAREN expr RPAREN
                        | variable
empty                   :
"""
class Parser:
    def __init__(self, tokens):
        """tokens is a generator"""
        self.tokens = tokens
        self.current_token = None
        self.get_next_token()

    def get_next_token(self):
        self.current_token = next(self.tokens, Lexer.end_of_file)

    def eat(self, type):
        if type == self.current_token.type:
            self.get_next_token()
        else:
            raise TypeError(f'Expected {type}, got {self.current_token.type}')

    def parse_program(self):
        return self.program()

    def parse(self):
        return self.expr()

    def expr(self):
        result = self.term()

        while self.current_token.type in (PLUS, MINUS):
            if self.current_token.type == PLUS:
                token = self.current_token
                self.eat(PLUS)
                result = BinaryOp(token, result, self.term())
            else:
                token = self.current_token
                self.eat(MINUS)
                result = BinaryOp(token, result, self.term())

        return result

    def term(self):
        result = self.factor()

        while self.current_token.type in (TIMES, DIVIDE, INTEGER_DIVIDE):
            if self.current_token.type == TIMES:
                token = self.current_token
                self.eat(TIMES)
                result = BinaryOp(token, result, self.factor())
            elif self.current_token.type == DIVIDE:
                token = self.current_token
                self.eat(DIVIDE)
                result = BinaryOp(token, result, self.factor())
            else:
                token = self.current_token
                self.eat(INTEGER_DIVIDE)
                result = BinaryOp(token, result, self.factor())
        return result

    def factor(self):
        if self.current_token.type in (PLUS, MINUS):
            if self.current_token.type == PLUS:
                token = self.current_token
                self.eat(PLUS)
                result = UnaryOp(token, self.factor())
            else:
                token = self.current_token
                self.eat(MINUS)
                result = UnaryOp(token, self.factor())
        elif self.current_token.type == LPAREN:
            self.eat(LPAREN)
            result = self.expr()
            self.eat(RPAREN)
        elif self.current_token.type == NUMBER:
            result = Number(self.current_token)
            self.eat(NUMBER)
        elif self.current_token.type == VARIABLE:
            result = self.variable()
        else:
            raise TypeError(f'Expected one of (PLUS, MINUS, LPAREN, NUMBER), got {self.current_token.type}')

        return result

    def program(self):
        result = self.compound_statement()
        self.eat(DOT)
        return result

    def compound_statement(self):
        self.eat(BEGIN)
        result = Compound(self.statement_list())
        logging.debug(self.current_token)
        self.eat(END)
        return result

    def statement_list(self):
        result = [self.statement()]
        if self.current_token.type == SEMICOLON:
            self.eat(SEMICOLON)
            result.extend(self.statement_list())
        return result

    def statement(self):
        if self.current_token.type == BEGIN:
            result = self.compound_statement()
        elif self.current_token.type == VARIABLE:
            result = self.assignment_statement()
        else:
            result = NoOp()
        return result

    def assignment_statement(self):
        var = self.variable()
        assignment_op = self.current_token
        self.eat(ASSIGN)
        logging.debug(assignment_op)
        return Assignment(assignment_op, var, self.expr())

    def variable(self):
        var = Variable(self.current_token)
        self.eat(VARIABLE)
        return var
