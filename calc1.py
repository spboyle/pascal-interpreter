#!/usr/bin/env python
# Token types
#
# EOF (end-of-file) token: no more input left for lexical analysis
INTEGER = 'INTEGER'
PLUS, MINUS =  'PLUS', 'MINUS'
EOF = 'EOF'


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
        self.current_token = None

    def error(self):
        raise Exception('Error parsing input')

    def get_next_character(self):
        current_char = ''
        while not current_char and self.pos < len(self.text):
            current_char = self.text[self.pos].strip()
            self.pos += 1
        return current_char

    def get_next_token(self):
        current_char = self.get_next_character()
        if not current_char:
            return Token(EOF, None)

        if current_char.isdigit():
            number_token = current_char
            while self.pos < len(self.text) and self.text[self.pos].isdigit():
                number_token += self.get_next_character()

            token = Token(INTEGER, int(number_token))
            return token

        if current_char == '+':
            token = Token(PLUS, current_char)
            return token
        elif current_char == '-':
            token = Token(MINUS, current_char)
            return token

        self.error()

    def eat(self, token_type):
        if self.current_token.token_type == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error()

    def expr(self):
        self.current_token = self.get_next_token()

        left = self.current_token
        self.eat(INTEGER)

        operator = self.current_token
        if operator.token_type == PLUS:
            self.eat(PLUS)
        elif operator.token_type == MINUS:
            self.eat(MINUS)

        right = self.current_token
        self.eat(INTEGER)

        if operator.token_type == PLUS:
            result = left.value + right.value
        elif operator.token_type == MINUS:
            result = left.value - right.value

        return result


def main():
    while True:
        try:
            text = input('calc> ')
        except EOFError:
            break
        if not text:
            continue
        interpreter = Interpreter(text)
        result = interpreter.expr()
        print(result)


if __name__=='__main__':
    main()
