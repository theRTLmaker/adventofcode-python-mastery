import sys
import os

# Add the parent directory to sys.path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from progress_bar import progress_bar

# -------- Day 24 --------

def parse_file(file_path):
    # Dictionaries to store the first part (key-value pairs)
    variables = {}
    # List to store the second part (operations)
    operations = []
    operations_d = {}

    with open(file_path, 'r') as file:
        lines = file.readlines()

        # Parse the first section
        for line in lines:
            line = line.strip()
            if not line:  # Skip blank lines
                continue
            if ':' in line:
                left, right = line.split(':')
                variables[left.strip()] = int(right.strip())
            elif '->' in line:  # Parse the second section
                inputs, output = line.split('->')
                inputs = inputs.strip().split()
                operations.append((inputs, output.strip()))
                operations_d[output.strip()] = inputs

    return variables, operations, operations_d

def convert_to_binary(n, length=47):
    """
    Convert a base-10 number `n` to a binary string of specified length.
    """
    binary_str = bin(n)[2:]  # Remove the "0b" prefix
    return binary_str.zfill(length)  # Ensure it is the specified length (47 bits)

def update_variables_from_input(variables, x_value, y_value):
    """
    Update the variables dictionary with the provided x and y values.
    The values are assumed to be base 10 numbers that will be converted to binary.
    """
    # Convert the base 10 numbers to binary and update the dictionary
    for i in reversed(range(47)):  # Assuming x and y variables go from x00 to x46, and y00 to y46
        variables[f'x{i:02d}'] = int(x_value[46-i])
        variables[f'y{i:02d}'] = int(y_value[46-i])
    return variables

# Usage Example
file_path = "day24.txt"  # Path to your text file
variables, operations, operations_d = parse_file(file_path)

# Outputs
# print("Variables:", variables)
# print("Operations:", operations)
# print("Operations:", operations_d)

# Get command line arguments for x and y
if len(sys.argv) == 3:
    x_value = int(sys.argv[1])  # Base 10 number for x
    y_value = int(sys.argv[2])  # Base 10 number for y

    # Convert the base 10 numbers to 47-bit binary
    x_binary = convert_to_binary(x_value)
    y_binary = convert_to_binary(y_value)
    print("Overwriting inputs")
    print(x_binary, y_binary)

    # Update the variables dictionary with the binary values
    variables = update_variables_from_input(variables, x_binary, y_binary)

x_list = []
y_list = []
for var, data in variables.items():
    if var.startswith('x'):
        x_list.append(data)
    if var.startswith('y'):
        y_list.append(data)

z_list = []
targets = set()
for input, output in operations:
    if output.startswith('z'):
        z_list.append(output)
    targets.add(output)
z_list = list(reversed(sorted(z_list)))

# ----- part 1 -----
print("-------------")
print("Part 1")

from functools import cache

@cache
def compute(target):
    if target in variables:
        return variables[target]

    for input, output in operations:
        if output == target:
            a, op, b = input
            if op == "AND":
                return compute(a) & compute(b)
            elif op == 'OR':
                return compute(a) | compute(b)
            else:
                return compute(a) ^ compute(b)

number = []
for output in z_list:
    result = compute(output)
    number.append(result)
    # print(output, result)

joined_number = ''.join(map(str, number))
print(f"Final number is {joined_number}={int(joined_number, 2)}")


# ----- part 2 -----
print("-------------")
print("Part 2")

def swap_dict_content(d, key_pairs):
    for key1, key2 in key_pairs:
        # Swap the values between key1 and key2
        if key1 in d and key2 in d:
            d[key1], d[key2] = d[key2], d[key1]
    return d

key_pairs = [
    ('qjb', 'gvw'),
    ('jgc', 'z15'),
    ('drg', 'z22'),
    ('jbp', 'z35')
]

operations_d = swap_dict_content(operations_d, key_pairs)

# @cache
def compute_d(target):
    if target in variables:
        return variables[target]

    for output, input in operations_d.items():
        if output == target:
            a, op, b = input
            if op == "AND":
                return compute_d(a) & compute_d(b)
            elif op == 'OR':
                return compute_d(a) | compute_d(b)
            else:
                return compute_d(a) ^ compute_d(b)

z_list = []
targets = set()
for input, output in operations:
    if output.startswith('z'):
        z_list.append(output)
    targets.add(output)
z_list = list(reversed(sorted(z_list)))

number = []
for output in z_list:
    result = compute_d(output)
    number.append(result)

joined_number = ''.join(map(str, number))
print(f"Final number is {joined_number}={int(joined_number, 2)}")
assert (int(joined_number, 2) == (x_value + y_value))
