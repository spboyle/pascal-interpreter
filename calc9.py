#!/usr/bin/env python


from collections import namedtuple
import operator
import string
import traceback

Token = namedtuple('Token', ('type', 'value'))
EOF = 'EOF'
NUMBER, PLUS, MINUS, TIMES, DIVIDE, LPAREN, RPAREN = (
    'NUMBER', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'LPAREN', 'RPAREN',
)
ASSIGN, VARIABLE, SEMICOLON, DOT, BEGIN, END = 'ASSIGN', 'VARIABLE', 'SEMICOLON', 'DOT', 'BEGIN', 'END'

RESERVED_WORDS = {
    BEGIN,
    END
}
"""
Lexical Analysis
"""
class Lexer:
    operations = {
        '+': Token(PLUS, '+'),
        '-': Token(MINUS, '-'),
        '*': Token(TIMES, '*'),
        '/': Token(DIVIDE, '/'),
        '(': Token(LPAREN, '('),
        ')': Token(RPAREN, ')'),
    }
    end_of_file = Token(EOF, None)
    assignment_token = Token(ASSIGN, ':=')
    semicolon = Token(SEMICOLON, ';')
    dot = Token(DOT, '.')

    reserved_words = {
        BEGIN: Token(BEGIN, BEGIN),
        END: Token(END, END),
    }

    acceptable_var_chars = string.ascii_letters + string.digits + '_'

    def __init__(self, text):
        self.text = text
        self.reset()

    def reset(self):
        self.pos = 0
        self.current_char = self.text[self.pos]

    def advance(self):
        self.pos += 1
        try:
            self.current_char = self.text[self.pos]
        except IndexError:
            self.current_char = ''

    def peek(self):
        try:
            return self.text[self.pos + 1]
        except IndexError:
            return ''

    def _id(self):
        result = ''
        if self.current_char in string.ascii_letters:
            while self.current_char and self.current_char in self.acceptable_var_chars:
                result += self.current_char
                self.advance()
        return result

    def identifier(self):
        identifier = self._id()
        if identifier:
            return self.reserved_words.get(identifier, Token(VARIABLE, identifier))

    def assignment(self):
        if self.current_char == ':':
            self.advance()
            if self.current_char == '=':
                token = ':='
                self.advance()
                return token

    def number(self):
        result = ''
        decimal_found = self.current_char == '.'
        while self.current_char.isdigit() or (not decimal_found and self.current_char == '.'):
            result += self.current_char
            self.advance()

        return result

    def get_next_token(self):
        while self.current_char.isspace():
            self.advance()
        if self.current_char == '':
            return self.end_of_file
        elif self.current_char == ';':
            self.advance()
            return self.semicolon
        elif self.current_char == '.':
            self.advance()
            return self.dot
        elif (identifier := self.identifier()):
            return identifier
        elif (number := self.number()):
            return Token(NUMBER, number)
        elif (assignment := self.assignment()):
            return self.assignment_token
        elif self.current_char in self.operations:
            token = self.operations[self.current_char]
            self.advance()
            return token
        else:
            raise ValueError(f'Unexpected character {self.current_char}')

    def tokenize(self):
        self.reset()
        while (token := self.get_next_token()).type != EOF:
            yield token


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

class Assign(BinaryOp):
    pass

class Var(Number):
    pass

class NoOp(AST):
    pass

class Compound(AST):
    def __init__(self, children=None):
        self.children = children or []


"""
Syntax Analysis
program                 : compound_statement DOT
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

        while self.current_token.type in (TIMES, DIVIDE):
            if self.current_token.type == TIMES:
                token = self.current_token
                self.eat(TIMES)
                result = BinaryOp(token, result, self.factor())
            else:
                token = self.current_token
                self.eat(DIVIDE)
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
        self.eat(END)
        return result

    def statement_list(self):
        result = [self.statement()]
        if self.current_token.type == SEMI:
            self.eat(SEMI)
            result.extend(self.statement_list())
        return result

    def statement(self):
        if self.current_token.type == BEGIN:
            result = self.compound_statement()
        elif self.current_token.type == VARIABLE:
            result = self.assignment_statment()
        else:
            result = NoOp()
        return result

    def assignment_statement(self):
        var = self.variable()
        assignment_op = self.current_token
        self.eat(ASSIGN)
        return Assign(assignment_op, var, self.expr())

    def variable(self):
        var = Variable(self.current_token)
        self.eat(VARIABLE)
        return var

"""
Visitor pattern, AST evaluation
"""
class Interpreter:
    binary_operations = {
        PLUS: operator.add,
        MINUS: operator.sub,
        TIMES: operator.mul,
        DIVIDE: operator.truediv,
    }

    unary_operations = {
        PLUS: lambda x: x,
        MINUS: lambda x: -x,
    }

    def __init__(self, ast):
        self.ast = ast

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


if __name__ == '__main__':
    while not (text := input('calc9> ')).startswith('exit'):
        try:
            lexer = Lexer(text)
            parser = Parser(lexer.tokenize())
            interpreter = Interpreter(parser.parse())
            print(interpreter.interpret())
        except:
            traceback.print_exc()
