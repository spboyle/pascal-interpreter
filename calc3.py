#!/usr/bin/env python

"""
This is a re-creation of lexer (lexical analyzer, tokenizer, scanner)
and parser (syntax analyzer) which handles binary operations +, -, *, /,
and integers
"""

from traceback import print_exc

INTEGER = 'INTEGER'
EOF = 'EOF'
PLUS, MINUS, TIMES, DIVIDE = 'PLUS', 'MINUS', 'TIMES', 'DIVIDE'


class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return 'Token({}, {})'.format(self.type, self.value)

    def __repr__(self):
        return str(self)


class Lexer:
    def __init__(self, text):
        self.text = text.strip()
        self.index = 0
        self.current_char = self.text[self.index]

    def advance(self):
        """
        Sets self.current_char to the next non-whitespace character
        """
        # Set to blank in case we are at end of text
        self.current_char = ''
        self.index += 1
        while self.index < len(self.text) and not (self.text[self.index].strip()):
            self.index += 1

        self.current_char = self.text[self.index] if self.index < len(self.text) else ''

    def integer(self):
        """
        Advances self.current_char through consecutive numbers, concatenating them
        into a single integer token
        """
        result = ''
        while self.index < len(self.text) and self.text[self.index].isdigit():
            result += self.text[self.index]
            self.index += 1

        # Reset self.current_char to where self.index is pointing
        self.current_char = self.text[self.index] if self.index < len(self.text) else ''
        return int(result)

    def tokens(self):
        while self.current_char:
            if self.current_char.isdigit():
                token = Token(INTEGER, self.integer())
            elif self.current_char == '+':
                token = Token(PLUS, self.current_char)
            elif self.current_char == '-':
                token = Token(MINUS, self.current_char)
            elif self.current_char == '*':
                token = Token(TIMES, self.current_char)
            elif self.current_char == '/':
                token = Token(DIVIDE, self.current_char)
            else:
                raise Exception('Unhandled character: {}'.format(self.current_char))
            self.advance()
            yield token


class Parser:
    def __init__(self, lexer):
        self.tokens = lexer.tokens()
        self.get_next_token()

    def get_next_token(self):
        self.current_token = next(self.tokens, Token(EOF, EOF))

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.get_next_token()
        else:
            raise Exception('Expected token {}, got {}'.format(token_type, self.current_token.type))

    def factor(self):
        token = self.current_token
        self.eat(INTEGER)
        return token.value

    def term(self):
        result = self.factor()

        while self.current_token.type in [TIMES, DIVIDE]:
            if self.current_token.type == TIMES:
                self.eat(TIMES)
                result *= self.factor()
            else:
                self.eat(DIVIDE)
                result /= self.factor()

        return result

    def expr(self):
        result = self.term()

        while self.current_token.type in [PLUS, MINUS]:
            if self.current_token.type == PLUS:
                self.eat(PLUS)
                result += self.term()
            else:
                self.eat(MINUS)
                result -= self.term()

        return result

    def evaluate(self):
        return self.expr()



if __name__ == '__main__':
    thing = '54 - 8'
    lexer = Lexer(thing)
    parser = Parser(lexer)
    print(parser.evaluate())
    # print(tokens)

    thing = '    54 * 8 -     78889 + 22 / 444 *  9     '
    lexer = Lexer(thing)
    parser = Parser(lexer)
    print(parser.evaluate())
    # print(tokens)

    while not (text := input('calc3> ')).startswith('exit'):
        try:
            print(Parser(Lexer(text)).evaluate())
        except Exception:
            print_exc()
