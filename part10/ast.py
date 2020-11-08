#!/usr/bin/env python

"""
Abstract Syntax Tree
"""
class AST:
    pass


class BinaryOp(AST):
    def __init__(self, token, left, right):
        self.token = token
        self.left = left
        self.right = right


class UnaryOp(AST):
    def __init__(self, token, operand):
        self.token = token
        self.operand = operand


class Number(AST):
    def __init__(self, token):
        self.token = token
        self.value = self.token.value


class Assignment(BinaryOp):
    pass


class Variable(Number):
    pass


class NoOp(AST):
    pass


class Compound(AST):
    def __init__(self, children=None):
        self.children = children or []
