class Operator:

    def __init__(self, symbol, precedence, associativity, arity, function):
        self.symbol = symbol
        self.precedence = precedence
        self.associativity = associativity
        self.arity = arity
        self.function = function

operators = {"+": Operator("+", 0, "L", 2, (lambda a, b: a + b)),
             "-": Operator("-", 0, "L", 2, (lambda a, b: a - b)),
             "*": Operator("*", 1, "L", 2, (lambda a, b: a * b)),
             "/": Operator("/", 1, "L", 2, (lambda a, b: a / b))}

class Stack:
    
    def __init__(self):
        self.stack = []
    
    def push(self, value):
        self.stack.append(value)
    
    def pop(self):
        return self.stack.pop()
    
    def peek(self):
        return self.stack[-1]

def shunting_yard(tokens):
    operator_stack = Stack()
    output_queue = []
    for i, token in enumerate(tokens):
        if token.isnumeric():
            output_queue.append(token)
        elif token in operators:
            if len(operator_stack.stack) == 0:
                operator_stack.push(token)
            else:
                top = operator_stack.peek()
                if top not in operators:
                    operator_stack.push(token)
                    continue
                if operators[token].precedence > operators[top].precedence:
                    operator_stack.push(token)
                elif operators[token].precedence <= operators[top].precedence and operators[token].associativity == "L":
                    while len(operator_stack.stack) > 0 and operator_stack.peek() in operators and operators[operator_stack.peek()].precedence >= operators[token].precedence:
                        output_queue.append(operator_stack.pop())
                    operator_stack.push(token)
        elif token == "(":
            operator_stack.push(token)
        elif token == ")":
            while operator_stack.peek() != "(":
                output_queue.append(operator_stack.pop())
            if operator_stack.peek() == "(":
                operator_stack.pop()

    while len(operator_stack.stack) > 0:
        output_queue.append(operator_stack.pop())

    return output_queue

def evaluate_postfix(tokens):
    result_stack = Stack()
    for token in tokens:
        if token.isnumeric():
            result_stack.push(int(token))
        elif token in operators:
            popped_values = []
            for _ in range(operators[token].arity):
                popped_values.append(result_stack.pop())
            if operators[token].arity == 2:
                a, b = popped_values
                function = operators[token].function
                result_stack.push(function(int(a), int(b)))

    return result_stack.peek()

def evaluate_expression(expression):
    expression = expression.split()
    return evaluate_postfix(shunting_yard(expression))

