def parse_rtl_description(descriptions):
    """
    Parse the RTL description into a structured list of operations.

    Args:
        descriptions (list of str): List of RTL descriptions.

    Returns:
        list of dict: Parsed descriptions.
    """
    parsed = []
    for desc in descriptions:
        parts = desc.split()
        if len(parts) == 5 and parts[1] in {"AND", "OR", "XOR"} and parts[3] == "->":
            parsed.append({
                "input1": parts[0],
                "op": parts[1],
                "input2": parts[2],
                "output": parts[4],
            })
        else:
            raise ValueError(f"Invalid description format: {desc}")
    return parsed

def build_signal_chains(parsed_descriptions):
    """
    Build a data structure representing the chains of signals.

    Args:
        parsed_descriptions (list of dict): Parsed descriptions.

    Returns:
        dict: A mapping of outputs to their gate descriptions.
    """
    chains = {}
    for gate in parsed_descriptions:
        chains[gate["output"]] = gate
    return chains

def generate_ascii_gate(gate):
    """
    Generate ASCII art for a single logic gate operation.

    Args:
        gate (dict): Logic gate operation with inputs and output.

    Returns:
        str: ASCII art representation.
    """
    templates = {
        "AND": "{input1} ----|\n       | AND |---- {output}\n{input2} ----|/",
        "OR":  "{input1} ----|\n       |  OR |---- {output}\n{input2} ----|/",
        "XOR": "{input1} ----|\n      )| XOR |---- {output}\n{input2} ----|/",
    }

    template = templates.get(gate["op"])
    if not template:
        raise ValueError(f"Unsupported operation: {gate['op']}")

    return template.format(
        input1=gate["input1"].ljust(6),
        input2=gate["input2"].ljust(6),
        output=gate["output"].ljust(6),
    )

def generate_ascii_from_chains(chains):
    """
    Generate ASCII art for the entire design based on signal chains.

    Args:
        chains (dict): Signal chain data structure.

    Returns:
        str: Combined ASCII art for the entire design.
    """
    visited = set()

    def generate_nested(signal, depth=0):
        if signal not in chains:
            return signal.ljust(6)
        if signal in visited:
            return signal.ljust(6)

        visited.add(signal)
        gate = chains[signal]

        input1_ascii = generate_nested(gate["input1"], depth + 1)
        input2_ascii = generate_nested(gate["input2"], depth + 1)

        spacer = " " * (depth * 4)
        gate_ascii = (
            f"{input1_ascii} ----|\n"
            f"{spacer}   | {gate['op']} |---- {signal.ljust(6)}\n"
            f"{input2_ascii} ----|/"
        )

        if depth > 0:
            gate_ascii = f"{spacer}|\n" + gate_ascii + f"\n{spacer}|"

        return gate_ascii

    # Find all final outputs (e.g., signals starting with 'z')
    final_outputs = [sig for sig in chains if sig.startswith("z")]

    # Generate ASCII for each final output
    result = []
    for output in final_outputs:
        result.append(generate_nested(output))

    return "\n\n".join(result)

def generate_ascii_art(rtl_descriptions):
    """
    Generate ASCII art for a list of RTL descriptions.

    Args:
        rtl_descriptions (list of str): List of RTL descriptions.

    Returns:
        str: Combined ASCII art for the entire design.
    """
    parsed_descriptions = parse_rtl_description(rtl_descriptions)
    chains = build_signal_chains(parsed_descriptions)
    return generate_ascii_from_chains(chains)

def read_rtl_file(file_path):
    """
    Read RTL descriptions from a file.

    Args:
        file_path (str): Path to the input file.

    Returns:
        list of str: Lines from the file.
    """
    with open(file_path, 'r') as file:
        return [line.strip() for line in file if line.strip()]

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python rtl_ascii_art.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]

    try:
        rtl_description = read_rtl_file(input_file)
        art = generate_ascii_art(rtl_description)
        print(art)
    except Exception as e:
        print(f"Error: {e}")
