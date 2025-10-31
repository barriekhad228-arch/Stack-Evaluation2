# main.py
# Stack-Based Expression Evaluator

class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop() if not self.is_empty() else None

    def peek(self):
        return self.items[-1] if not self.is_empty() else None

    def is_empty(self):
        return len(self.items) == 0


def precedence(op):
    if op in ('+', '-'):
        return 1
    if op in ('*', '/'):
        return 2
    return 0


def apply_operator(operators, values):
    right = values.pop()
    left = values.pop()
    op = operators.pop()

    if op == '+':
        values.push(left + right)
    elif op == '-':
        values.push(left - right)
    elif op == '*':
        values.push(left * right)
    elif op == '/':
        values.push(left / right)


def evaluate_expression(expression):
    operators = Stack()
    values = Stack()
    i = 0

    while i < len(expression):
        char = expression[i]

        if char == ' ':
            i += 1
            continue

        if char.isdigit():
            num = 0
            while i < len(expression) and expression[i].isdigit():
                num = num * 10 + int(expression[i])
                i += 1
            values.push(num)
            i -= 1

        elif char == '(':
            operators.push(char)

        elif char == ')':
            while not operators.is_empty() and operators.peek() != '(':
                apply_operator(operators, values)
            operators.pop()

        elif char in ['+', '-', '*', '/']:
            while (not operators.is_empty() and 
                   precedence(operators.peek()) >= precedence(char)):
                apply_operator(operators, values)
            operators.push(char)

        i += 1

    while not operators.is_empty():
        apply_operator(operators, values)

    return values.pop()


def process_files(input_file, output_file):
    with open(input_file, 'r') as infile:
        lines = infile.readlines()

    results = []
    for line in lines:
        line = line.strip()
        if line == "-----":
            results.append("-----")
        elif line:
            result = evaluate_expression(line)
            results.append(str(int(result)))

    with open(output_file, 'w') as outfile:
        for res in results:
            outfile.write(res + "\n")


if __name__ == "__main__":
    process_files("input.txt", "output.txt")
    print("Evaluation complete. Check output.txt for results.")
