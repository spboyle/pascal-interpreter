#!/usr/bin/env python
# Token types
#
# EOF (end-of-file) token: no more input left for lexical analysis
INTEGER = 'INTEGER'
PLUS, MINUS, TIMES, DIVIDE =  'PLUS', 'MINUS', 'TIMES', 'DIVIDE'
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

        self.error()

    def eat(self, token_type):
        if self.current_token.token_type == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error()

    def expr(self):
        self.current_token = self.get_next_token()

        operand_stack = []
        left = self.current_token
        self.eat(INTEGER)

        operand_stack.append(left)
        while self.current_token.token_type != EOF:
            if self.current_token.token_type == TIMES:
                if not operand_stack:
                    self.error()
                self.eat(TIMES)
                left_operand = operand_stack.pop()
                right_operand = self.current_token
                self.eat(INTEGER)
                operand_stack.append(Token(INTEGER, left_operand.value * right_operand.value))
            elif self.current_token.token_type == DIVIDE:
                if not operand_stack:
                    self.error()
                self.eat(DIVIDE)
                left_operand = operand_stack.pop()
                right_operand = self.current_token
                self.eat(INTEGER)
                operand_stack.append(Token(INTEGER, left_operand.value / right_operand.value))

            elif self.current_token.token_type == PLUS:
                if not operand_stack:
                    self.error()
                self.eat(PLUS)
                left_operand = operand_stack.pop()
                right_operand = self.current_token
                self.eat(INTEGER)
                # If next token has higher precedence, save current operation on the stack
                if self.current_token.token_type in [TIMES, DIVIDE]:
                    operand_stack.append(left_operand)
                    operand_stack.append(Token(PLUS, '+'))
                    operand_stack.append(right_operand)
                else:
                    operand_stack.append(Token(INTEGER, left_operand.value + right_operand.value))

            elif self.current_token.token_type == MINUS:
                if not operand_stack:
                    self.error()
                self.eat(MINUS)
                left_operand = operand_stack.pop()
                right_operand = self.current_token
                self.eat(INTEGER)
                # If next token has higher precedence, save current operation on the stack
                if self.current_token.token_type in [TIMES, DIVIDE]:
                    operand_stack.append(left_operand)
                    operand_stack.append(Token(MINUS, '-'))
                    operand_stack.append(right_operand)
                else:
                    operand_stack.append(Token(INTEGER, left_operand.value - right_operand.value))

        while len(operand_stack) > 2:
            right = operand_stack.pop()
            operator = operand_stack.pop()
            left = operand_stack.pop()

            if operator.token_type == PLUS:
                operand_stack.append(Token(INTEGER, left.value + right.value))
            elif operator.token_type == MINUS:
                operand_stack.append(Token(INTEGER, left.value - right.value))

        if operand_stack:
            result = operand_stack.pop().value
        else:
            self.error('There should be a token on the stack')

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
