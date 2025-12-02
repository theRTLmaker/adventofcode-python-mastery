import re

def extract_number(signal):
    """
    Extract the number from a signal name.
    """
    match = re.search(r'\d+', signal)
    return int(match.group()) if match else None

def generate_aliases(operations):
    """
    Generate aliases for outputs based on the numbers in the inputs if both match.
    """
    alias_map = {}

    for inputs, output in operations:
        input1, operator, input2 = inputs[0], inputs[1], inputs[2]

        # Extract numbers from inputs
        number1 = extract_number(input1)
        number2 = extract_number(input2)

        # Only generate alias if both numbers exist and match
        if number1 is not None and number2 is not None and number1 == number2:
            alias = f"{operator.upper()}{number1}"
            alias_map[output] = alias

    return alias_map

def apply_aliases(operations, alias_map, final : bool):
    """
    Apply aliases to all operations, renaming inputs and outputs.
    """
    processed_lines = []

    for inputs, output in operations:
        if not type(inputs) is list:
            inputs = inputs.split(" ")
        input1, operator, input2 = inputs[0], inputs[1], inputs[2]

        # Replace inputs and output with aliases if they exist
        input1 = alias_map.get(input1, input1)
        input2 = alias_map.get(input2, input2)
        output = alias_map.get(output, output)

        # Create the renamed line
        if final:
            renamed_line = f"{input1} {operator} {input2} -> {output}"
        else:
            renamed_line = (f"{input1} {operator} {input2}", output)
        processed_lines.append(renamed_line)

    return processed_lines

def replace_regex(lines, pattern, replacement):
    """
    Perform a regex find and replace on a list of lines.
    """
    for i in range(50):
        replaced_lines = []

        for line in lines:
            new_line = (re.sub(pattern, replacement, line[0]), re.sub(pattern, replacement, line[1]))

            replaced_lines.append(new_line)
        lines = replaced_lines

    return replaced_lines


def generate_intermediate_aliases(lines):
    """
    Generate the final aliases for CARRY_INTERMEDIATE(N) based on the pattern.

    Returns:
        list: A list of generated alias mappings.
    """
    alias_mappings = {}

    for inputs, output in lines:
        line = f"{inputs} -> {output}"
        match = re.match(r'(XOR(\d+)) AND (CARRY(\d+)) -> (\S+)', line)
        if match:
            xor_signal, n, carry_signal, n_minus_1, output = match.groups()
            if int(n) - 1 == int(n_minus_1):
                intermediate_alias = f"CARRY_INTERMEDIATE{n}"
                alias_mappings[output] = intermediate_alias
        else:
            match = re.match(r'(CARRY(\d+)) AND (XOR(\d+)) -> (\S+)', line)
            if match and match.groups()[0] == "CARRY1":
                breakpoint
            if match:
                carry_signal, n_minus_1, xor_signal, n, output = match.groups()
                if int(n) - 1 == int(n_minus_1):
                    intermediate_alias = f"CARRY_INTERMEDIATE{n}"
                    alias_mappings[output] = intermediate_alias

    return alias_mappings

def generate_final_aliases(lines):
    """
    Generate the final aliases for CARRY(N) based on the pattern.

    Returns:
        list: A list of generated alias mappings.
    """
    alias_mappings = {}

    for inputs, output in lines:
        line = f"{inputs} -> {output}"
        match = re.match(r'(CARRY(\d+)) OR (CARRY_INTERMEDIATE(\d+)) -> (\S+)', line)
        if match:
            xor_signal, n, carry_signal, n_other, output = match.groups()
            if int(n) == int(n_other):
                intermediate_alias = f"CARRY{n}"
                alias_mappings[output] = intermediate_alias
        else:
            match = re.match(r'(CARRY_INTERMEDIATE(\d+)) OR (CARRY(\d+)) -> (\S+)', line)
            if match:
                carry_signal, n_other, xor_signal, n, output = match.groups()
                if int(n) == int(n_other):
                    intermediate_alias = f"CARRY{n}"
                    alias_mappings[output] = intermediate_alias

    return alias_mappings

def apply_intermediate_aliases(lines, alias_mappings):
    """
    Apply the final aliasing rules for CARRY_INTERMEDIATE(N) and CARRY(N) to the lines.
    """
    processed_lines = []

    for line in lines:
        for intermediate_alias, xor_signal, carry_signal, final_alias in alias_mappings:
            if xor_signal in line and carry_signal in line:
                if f"{xor_signal} AND {carry_signal}" in line:
                    # Apply intermediate alias
                    line = f"{xor_signal} AND {carry_signal} -> {intermediate_alias}"
                    processed_lines.append(line)
                    # Apply final alias
                    line = f"AND{int(final_alias[-2:])} OR {intermediate_alias} -> {final_alias}"
                break
        else:
            processed_lines.append(line)

    return processed_lines

def process_operations(operations):
    """
    Generate aliases, apply them to the operations, perform regex replacement,
    and apply final aliasing rules.
    """
    # Step 1: Generate all aliases
    alias_map = generate_aliases(operations)

    # Step 2: Apply aliases to rename inputs and outputs
    processed_lines = apply_aliases(operations, alias_map, False)

    # Step 3: Perform regex replacement
    processed_lines = replace_regex(processed_lines, r'AND(\d{1,2})', r'CARRY\1')

    for i in range(250):
        # Step 4: Generate the final alias mappings
        alias_mappings = generate_intermediate_aliases(processed_lines)
        print(alias_mappings)

        # Step 5: Apply the final aliases to the lines
        processed_lines = apply_aliases(processed_lines, alias_mappings, False)

        alias_mappings = generate_final_aliases(processed_lines)
        print(alias_mappings)

        # Step 5: Apply the final aliases to the lines
        processed_lines = apply_aliases(processed_lines, alias_mappings, False)

    # Step 4: Generate the final alias mappings
    alias_mappings = generate_intermediate_aliases(processed_lines)
    print(alias_mappings)

    # Step 5: Apply the final aliases to the lines
    processed_lines = apply_aliases(processed_lines, alias_mappings, False)

    alias_mappings = generate_final_aliases(processed_lines)
    print(alias_mappings)

    # Step 5: Apply the final aliases to the lines
    processed_lines = apply_aliases(processed_lines, alias_mappings, True)

    return processed_lines


def write_output_file(processed_lines, output_file_path):
    """
    Write the processed lines to a new output file.
    """
    with open(output_file_path, 'w') as file:
        file.write('\n'.join(processed_lines) + '\n')


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

# Usage Example
file_path = "day24-fixed.txt"  # Path to your input text file
output_file_path = "day24_processed.txt"  # Path for the output text file

# Parse the file and process operations
variables, operations, operations_d = parse_file(file_path)
processed_lines = process_operations(operations)

import math

def extract_indices(line):
    """
    Extract all indices from signal names in a line.
    """
    matches = re.findall(r'\d+', line)  # Find all numbers in the line
    return [int(match) for match in matches]

def calculate_average_index(line):
    """
    Calculate the average index of a line, rounding upwards.
    Ignore signals without indices.
    """
    indices = extract_indices(line)
    if not indices:  # No indices found
        return float('inf')  # Sort lines without indices last
    average = sum(indices) / len(indices)
    return math.ceil(average)

def sort_lines_by_average_index(lines):
    """
    Sort lines by the average index of the signal names.
    """
    return sorted(lines, key=calculate_average_index)

def write_output_file_with_spacing(sorted_lines, output_file_path):
    """
    Write the sorted lines to the output file, appending an empty line
    between groups where the average index increases.
    """
    with open(output_file_path, 'w') as file:
        previous_index = None
        for line in sorted_lines:
            current_index = calculate_average_index(line)
            # Add an empty line if the average index increases
            if previous_index is not None and current_index > previous_index:
                file.write('\n')
            file.write(line + '\n')
            previous_index = current_index


sorted_lines = sort_lines_by_average_index(processed_lines)

# Write the processed lines to the output file
write_output_file_with_spacing(sorted_lines, output_file_path)
# write_output_file(processed_lines, output_file_path)
print(f"Processed file saved as {output_file_path}")
