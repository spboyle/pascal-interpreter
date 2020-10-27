#!/usr/bin/env python
# Token types
#
# EOF (end-of-file) token: no more input left for lexical analysis
INTEGER = 'INTEGER'
PLUS, MINUS, TIMES, DIVIDE =  'PLUS', 'MINUS', 'TIMES', 'DIVIDE'
EOF = 'EOF'


precedence_map = {
    'PLUS': 1,
    'MINUS': 1,
    'TIMES': 2,
    'DIVIDE': 2,
}


def precedence(operator_token):
    try:
        return precedence_map[operator_token.token_type]
    except KeyError:
        print("Precedence not found for {}".format(operator_token.token_type))
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

    @staticmethod
    def peek(stack):
        try:
            return stack[-1]
        except IndexError:
            return None

    def expr(self):
        self.current_token = self.get_next_token()

        stack = [self.current_token]
        self.eat(INTEGER)

        while self.current_token.token_type != EOF:
            # If current_token is an operand,
            # Look ahead at the following operation (advance current_token)
            # and look at the operation on the stack if present
            # to decide whether to crunch the numbers of this term or save them for later
            if self.current_token.token_type == INTEGER:
                current_operand = self.current_token
                self.eat(INTEGER)
                if (operator := self.peek(stack)):
                    if precedence(operator) >= precedence(self.current_token):
                        stack.append(self.crunch(stack.pop(), stack.pop(), current_operand))
                    else:
                        stack.append(current_operand)
            else:
                stack.append(self.current_token)
                self.eat(self.current_token.token_type)

        # Everything has been reduced to terms and Plus / Minus
        # Since it was put on a stack, the left-most operations are on the bottom
        # Reverse the stack and pull everything out
        # Probably so many ways to do this?
        stack.reverse()
        while len(stack) > 2:
            left, operator, right = stack.pop(), stack.pop(), stack.pop()
            stack.append(self.crunch(operator, left, right))

        if stack:
            result = stack.pop().value
        else:
            self.error('There should be a token on the stack')

        return result

    def crunch(self, operator, left, right):
        if operator.token_type == PLUS:
            return Token(INTEGER, left.value + right.value)
        elif operator.token_type == MINUS:
            return Token(INTEGER, left.value - right.value)
        elif operator.token_type == TIMES:
            return Token(INTEGER, left.value * right.value)
        elif operator.token_type == DIVIDE:
            return Token(INTEGER, left.value / right.value)


def main():
    while not (text := input('calc> ')).startswith('exit'):
        if not text:
            continue
        interpreter = Interpreter(text)
        result = interpreter.expr()
        print(result)


if __name__=='__main__':
    main()
