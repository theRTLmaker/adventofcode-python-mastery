import sys
import os

# Add the parent directory to sys.path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from progress_bar import progress_bar

# -------- Day 15 --------
import re

with open("day17.txt", "r") as file:
    text = file.read()

# Use regular expressions to extract register values
val_reg_a = int(re.search(r"Register A: (\d+)", text).group(1))
val_reg_b = int(re.search(r"Register B: (\d+)", text).group(1))
val_reg_c = int(re.search(r"Register C: (\d+)", text).group(1))

# Extract the program list
program = list(map(int, re.search(r"Program: ([\d,]+)", text).group(1).split(',')))

# Output the results
print("Register A:", val_reg_a)
print("Register B:", val_reg_b)
print("Register C:", val_reg_c)
print("Program:", program)

# ----- part 1 -----
print("-------------")
print("Part 1")

op_encoding = {
    0 : "adv",
    1 : "bxl",
    2 : "bst",
    3 : "jnz",
    4 : "bxc",
    5 : "out",
    6 : "bvd",
    7 : "cdv",
}
class Register:
    def __init__(self, value=0):
        self.value = value

class RegisterAPI:
    def __init__(self, registers):
        # Fixed encodings
        self.fixed_encodings = {
            0: 0,
            1: 1,
            2: 2,
            3: 3
        }
        # Registers passed in for dynamic access
        self.orig_registers = registers
        self.registers = registers

    def reset(self):
        self.registers = self.orig_registers

    def get(self, key):
        """Get the value of the given encoding."""
        if key in self.fixed_encodings:
            return self.fixed_encodings[key]
        elif key in self.registers:
            return self.registers[key].value
        else:
            raise KeyError(f"Key '{key}' not found in encodings or registers.")

    def set(self, key, value):
        """Set the value of the given encoding (only dynamic registers)."""
        if key in self.registers:
            self.registers[key].value = value
        else:
            raise KeyError(f"Key '{key}' is not writable or does not exist.")

# Create individual register variables
register_a = Register(val_reg_a)
register_b = Register(val_reg_b)
register_c = Register(val_reg_c)

# Map the registers to keys in the API
register_map = {
    4: register_a,
    5: register_b,
    6: register_c
}

# Create an instance of RegisterAPI
combo_enc = RegisterAPI(register_map)

# # Access values using both the API and direct variables
# print("Encoding '0':", combo_enc.get('0'))  # Fixed encoding
# print("Encoding '4' (Register A):", combo_enc.get('4'))  # Via API
# print("Direct Register A:", register_a.value)      # Direct access

# # Update a register through the API
# combo_enc.set('4', 123456)
# print("Updated Encoding '4' (Register A via API):", combo_enc.get('4'))
# print("Updated Direct Register A:", register_a.value)

# # Update the register directly
# register_a.value = 789012
# print("Updated Direct Register A (direct):", register_a.value)
# print("Updated Encoding '4' (via API):", combo_enc.get('4'))

def run_program():
    pc = 0
    outstream = []

    while pc < len(program):
        opcode = program[pc]
        operand = program[pc+1]
        # print("PC", pc)
        # print("Opcode", op_encoding[opcode])
        # print("operand", operand)

        inc_pc = True

        if op_encoding[opcode] ==  "adv":
            register_a.value = int(register_a.value / (2**combo_enc.get(operand)))
        elif op_encoding[opcode] ==  "bxl":
            register_b.value = register_b.value ^ operand
        elif op_encoding[opcode] ==  "bst":
            register_b.value = combo_enc.get(operand) % 8
        elif op_encoding[opcode] ==  "jnz":
            if register_a.value != 0:
                pc = operand
                inc_pc = False
        elif op_encoding[opcode] ==  "bxc":
            register_b.value = register_b.value ^ register_c.value
        elif op_encoding[opcode] ==  "out":
            outstream.append(str(combo_enc.get(operand) % 8))
        elif op_encoding[opcode] ==  "bvd":
            register_b.value = int(register_a.value / (2**combo_enc.get(operand)))
        elif op_encoding[opcode] ==  "cdv":
            register_c.value = int(register_a.value / (2**combo_enc.get(operand)))

        if inc_pc:
            pc += 2

        # print()
        # print("new PC", pc)
        # print("Register A:", register_a.value)
        # print("Register B:", register_b.value)
        # print("Register C:", register_c.value)
        # print()
        # print()
        # print()

    return outstream

outstream = run_program()
print("Output", ",".join(outstream))

# ----- part 2 -----
print("-------------")
print("Part 2")

def count_matching_indices(list1, list2):
    """
    Counts how many numbers match at the same index in two lists.

    Args:
        list1 (list of int): The first list of integers.
        list2 (list of int): The second list of integers.

    Returns:
        int: The count of matching numbers at the same indices.
    """
    # Use zip to pair elements at the same indices, and count matches
    return sum(1 for a, b in zip(list1, list2) if a == b)


def run_program2():
    pc = 0
    outstream = []

    while pc < len(program):
        opcode = program[pc]
        operand = program[pc+1]
        # print("PC", pc)
        # print("Opcode", op_encoding[opcode])
        # print("operand", operand)

        inc_pc = True

        if op_encoding[opcode] ==  "adv":
            register_a.value = int(register_a.value / (2**combo_enc.get(operand)))
        elif op_encoding[opcode] ==  "bxl":
            register_b.value = register_b.value ^ operand
        elif op_encoding[opcode] ==  "bst":
            register_b.value = combo_enc.get(operand) % 8
        elif op_encoding[opcode] ==  "jnz":
            if register_a.value != 0:
                pc = operand
                inc_pc = False
        elif op_encoding[opcode] ==  "bxc":
            register_b.value = register_b.value ^ register_c.value
        elif op_encoding[opcode] ==  "out":
            outstream.append(combo_enc.get(operand) % 8)
        elif op_encoding[opcode] ==  "bvd":
            register_b.value = int(register_a.value / (2**combo_enc.get(operand)))
        elif op_encoding[opcode] ==  "cdv":
            register_c.value = int(register_a.value / (2**combo_enc.get(operand)))

        if inc_pc:
            pc += 2

        # print()
        # print("new PC", pc)
        # print("Register A:", register_a.value)
        # print("Register B:", register_b.value)
        # print("Register C:", register_c.value)
        # print()
        # print()
        # print()

    return outstream

def process_integers_to_binary_and_back(int1, int2):
    # Step 1: Convert each integer to a 3-digit binary string
    binary_str1 = f"{int1:03b}"  # Format as a 3-digit binary
    binary_str2 = f"{int2:03b}"  # Format as a 3-digit binary
    print(binary_str1, binary_str2)
    # Step 2: Concatenate the two binary strings
    concatenated_binary_str = binary_str1 + binary_str2

    # Step 3: Convert the concatenated binary string back to an integer
    concatenated_binary_int = int(concatenated_binary_str, 2)

    return concatenated_binary_int

print("Program:", program)

def try_digit(reg_a, position):
    print("==-=-=-=-=-", position)
    reg_a = reg_a << 3
    for test_dig in range(8):
        test_value = reg_a + test_dig
        print("testing", test_dig, test_value)
        combo_enc.reset()
        register_a.value = test_value

        outstream = run_program2()
        if outstream[0] == program[position]:
            if position == 0:
                print("Program:", program)
                print("Output: ", outstream)
                print("Register A:", test_value)
                exit()
            try_digit(test_value, position - 1)

try_digit(0, len(program)-1)

print()
print("===========")
print("Register A:", val_reg_a)
print("Program:", program)
print("Output: ", [int(num) for num in outstream])