#!/usr/bin/env python
# Token types
#
# EOF (end-of-file) token: no more input left for lexical analysis
INTEGER = 'INTEGER'
PLUS, MINUS, TIMES, DIVIDE =  'PLUS', 'MINUS', 'TIMES', 'DIVIDE'
EOF = 'EOF'
DEBUG = False

precedence_map = {
    PLUS: 1,
    MINUS: 1,
    TIMES: 2,
    DIVIDE: 2,
    EOF: 2,
}


def debug(string):
    if DEBUG:
        print(string)

def precedence(operator_token):
    try:
        return precedence_map[operator_token.token_type]
    except KeyError:
        debug("Precedence not found for {}".format(operator_token.token_type))
        return -1


class Token():
    def __init__(self, token_type, value):
        self.token_type = token_type
        self.value = value

    def __str__(self):
        return 'Token({}, {})'.format(self.token_type, self.value)

    def __repr__(self):
        return self.__str__()


class Interpreter():
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_token = self.get_next_token()

    def error(self, msg='Error parsing input'):
        raise Exception(msg)

    def get_next_character(self):
        current_char = ''
        while not current_char and self.pos < len(self.text):
            current_char = self.text[self.pos].strip()
            self.pos += 1
        return current_char

    def integer(self, number_token):
        while self.pos < len(self.text) and self.text[self.pos].isdigit():
            number_token += self.get_next_character()

        return int(number_token)

    def get_next_token(self):
        current_char = self.get_next_character()
        if not current_char:
            return Token(EOF, None)

        if current_char.isdigit():
            return Token(INTEGER, self.integer(current_char))

        if current_char == '+':
            return Token(PLUS, current_char)
        elif current_char == '-':
            return Token(MINUS, current_char)
        elif current_char == '*':
            return Token(TIMES, current_char)
        elif current_char == '/':
            return Token(DIVIDE, current_char)

        self.error('Unexpected character {}'.format(current_char))

    def eat(self, token_type):
        if self.current_token.token_type == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error('Expected token type {}, got {}'.format(token_type, self.current_token.token_type))

    @staticmethod
    def peek(stack):
        try:
            return stack[-1]
        except IndexError:
            return None

    def number(self):
        token = self.current_token
        self.eat(INTEGER)
        return token.value

    def term(self):
        result = self.number()

        while self.current_token.token_type in (TIMES, DIVIDE):
            if self.current_token.token_type == TIMES:
                self.eat(TIMES)
                result *= self.number()
            elif self.current_token.token_type == DIVIDE:
                self.eat(DIVIDE)
                result /= self.number()

        return result

    def expr(self):
        result = self.term()

        while self.current_token.token_type in (PLUS, MINUS):
            if self.current_token.token_type == PLUS:
                self.eat(PLUS)
                result += self.term()
            elif self.current_token.token_type == MINUS:
                self.eat(MINUS)
                result -= self.term()

        return result


def main():
    while not (text := input('calc2> ')).startswith('exit'):
        if not text:
            continue
        interpreter = Interpreter(text)
        result = interpreter.expr()
        print(result)


if __name__=='__main__':
    main()
