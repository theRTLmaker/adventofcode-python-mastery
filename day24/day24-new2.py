

import re
from typing import List, Tuple, Dict

class WireAliasProcessor:
    def __init__(self):
        self.aliases: Dict[str, str] = {}

    def extract_number(self, wire: str) -> str:
        """Extract the numeric portion from a wire name."""
        match = re.search(r'\d+', wire)
        return match.group(0) if match else ''

    def create_alias_pattern(self, input1: str, operation: str, input2: str, alias: str) -> tuple:
        """Create a regex pattern for matching gates and their alias template."""
        # Convert patterns like "x(N)" to regex
        input1_pattern = input1.replace("(N)", r"(\d+)")
        input2_pattern = input2.replace("(N)", r"(\d+)")
        alias_template = alias.replace("(N)", "{}")

        pattern = f"{input1_pattern} {operation} {input2_pattern}"
        return re.compile(pattern), alias_template

    def apply_aliases(self, gates: List[Tuple[str, str]], alias_rules: List[Tuple[str, str, str, str]]) -> List[Tuple[str, str]]:
        """Apply alias rules to the gates list."""
        new_gates = []

        for input_expr, output_wire in gates:
            new_output = output_wire

            # Try each alias rule
            for input1, operation, input2, alias in alias_rules:
                pattern, alias_template = self.create_alias_pattern(input1, operation, input2, alias)
                print(input_expr, pattern, alias_template)
                match = pattern.match(input_expr)

                if match:
                    # If there's a match, create the alias using the number from the match
                    num = match.group(1)
                    new_output = alias_template.format(num)
                    self.aliases[output_wire] = new_output
                    break

            # Replace any known aliases in the input expression
            new_input = input_expr
            for old, new in self.aliases.items():
                new_input = new_input.replace(old, new)

            new_gates.append((new_input, new_output))

        return new_gates

    def sort_by_indices(self, gates: List[Tuple[str, str]]) -> List[Tuple[str, str]]:
        """Sort gates by the average of contained indices."""
        def get_avg_index(gate: Tuple[str, str]) -> float:
            # Extract all numbers from both input and output
            numbers = [int(num) for num in re.findall(r'\d+', gate[0] + gate[1])]
            return sum(numbers) / len(numbers) if numbers else float('inf')

        return sorted(gates, key=get_avg_index)

# Example usage
def process_gates(gates: List[Tuple[str, str]]) -> List[Tuple[str, str]]:
    processor = WireAliasProcessor()

    # First pass: AND and XOR aliases
    initial_aliases = [
        ("x(N)", "AND", "y(N)", "AND(N)"),
        ("x(N)", "XOR", "y(N)", "XOR(N)")
    ]
    gates = processor.apply_aliases(gates, initial_aliases)

    # Replace AND00 with CARRY00
    gates = [(input_expr.replace("AND00", "CARRY00"),
              output_wire.replace("AND00", "CARRY00"))
             for input_expr, output_wire in gates]

    # Second pass: CARRY_INTERMEDIATE and CARRY aliases
    carry_aliases = [
        ("XOR(N)", "AND", "CARRY(N-1)", "CARRY_INTERMEDIATE(N)"),
        ("AND(N)", "OR", "CARRY_INTERMEDIATE(N)", "CARRY(N)")
    ]
    gates = processor.apply_aliases(gates, carry_aliases)

    # Sort by indices
    gates = processor.sort_by_indices(gates)

    return gates

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
                inputs = inputs.strip()
                operations.append((inputs, output.strip()))
                operations_d[output.strip()] = inputs

    return variables, operations, operations_d

# Usage Example
file_path = "day24.txt"  # Path to your input text file
output_file_path = "day24_processed.txt"  # Path for the output text file

# Parse the file and process operations
variables, operations, operations_d = parse_file(file_path)
processed_gates = process_gates(operations)

processed_lines = []
for input_expr, output_wire in processed_gates:
    processed_lines.append(f"{input_expr} -> {output_wire}")

def write_output_file(processed_lines, output_file_path):
    """
    Write the processed lines to a new output file.
    """
    with open(output_file_path, 'w') as file:
        file.write('\n'.join(processed_lines) + '\n')


write_output_file(processed_lines, output_file_path)