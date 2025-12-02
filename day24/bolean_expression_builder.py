import sys

def parse_input(filename):
    with open(filename, 'r') as file:
        descriptions = file.readlines()

    expressions = {}
    for description in descriptions:
        description = description.strip()
        if description:  # Avoid empty lines
            parts = description.split(' -> ')
            left, right = parts[0], parts[1]
            a, op, b = left.split()
            expressions[right] = (a, op, b)
    return expressions

def build_expression(signal, expressions):
    if signal not in expressions:
        return signal  # Base case: the signal is just a signal, not an expression

    a, op, b = expressions[signal]
    if a.startswith("z"):
        a_expr = signal
    else:
        a_expr = build_expression(a, expressions)
    if b.startswith("z"):
        b_expr = signal
    else:
        b_expr = build_expression(b, expressions)

    return f"({a_expr} {op} {b_expr})"

def generate_boolean_expressions(filename):
    expressions = parse_input(filename)

    # Iterate through all the output signals and generate expressions for those starting with 'z'
    for output_signal in expressions:
        if output_signal.startswith('z'):
            expr = build_expression(output_signal, expressions)
            print(f"{output_signal} = {expr}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python generate_expression.py <filename>")
        sys.exit(1)

    filename = sys.argv[1]
    generate_boolean_expressions(filename)
