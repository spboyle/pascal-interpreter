#!/usr/bin/env python


from ast import *

"""
Visitor pattern, AST evaluation
"""
class Interpreter:
    binary_operations = {
        PLUS: operator.add,
        MINUS: operator.sub,
        TIMES: operator.mul,
        DIVIDE: operator.truediv,
        INTEGER_DIVIDE: operator.floordiv,
    }

    unary_operations = {
        PLUS: lambda x: x,
        MINUS: lambda x: -x,
    }

    def __init__(self, ast):
        self.ast = ast
        self.table = {}

    def interpret(self):
        return self.visit(self.ast)

    def visit(self, node):
        return getattr(self, f'visit_{type(node).__name__.lower()}')(node)

    def visit_binaryop(self, node):
        return self.binary_operations[node.token.type](self.visit(node.left), self.visit(node.right))

    def visit_unaryop(self, node):
        return self.unary_operations[node.token.type](self.visit(node.operand))

    def visit_number(self, node):
        try:
            return int(node.token.value)
        except ValueError:
            return float(node.token.value)

    def visit_compound(self, node):
        for child in node.children:
            self.visit(child)

        print(f'Result: {self.table}')
        return self.table

    def visit_assignment(self, node):
        var_value = node.left.value
        expr_value = self.visit(node.right)
        print(f'Assigning {var_value} = {expr_value}')
        self.table[var_value] = expr_value
        return expr_value

    def visit_variable(self, node):
        try:
            return self.table[node.value]
        except KeyError:
            raise NameError(f'{node.value} is not defined')

    def visit_noop(self, node):
        pass


if __name__ == '__main__':
    while not (text := input('calc9> ')).startswith('exit'):
        try:
            lexer = Lexer(text)
            parser = Parser(lexer.tokenize())
            interpreter = Interpreter(parser.parse())
            print(interpreter.interpret())
        except:
            traceback.print_exc()
