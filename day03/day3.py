# -------- Day 3 --------
# part 1
memory = []
with open("day3.txt", "r") as f:
    for line in f:
        memory.append(line)

import re

sum = 0

for i, line in enumerate(memory):
    matches = re.finditer(r"mul\((\d{1,3}),(\d{1,3})\)", line)
    for m in matches:
        print(f"Line {i+1}: Found match: {m.groups()}")
        sum += int(m.group(1)) * int(m.group(2))

print(sum)

# part 2
memory = []
with open("day3-2.txt", "r") as f:
    for line in f:
        memory.append(line)

enable = True
sum = 0

for i, line in enumerate(memory):
    matches = re.finditer(r"mul\((\d{1,3}),(\d{1,3})\)|don't|do", line)
    for m in matches:
        if m.group(1) and m.group(2):  # Match is "mul(...)"
            if enable:
                sum += int(m.group(1)) * int(m.group(2))
        elif m.group(0) == "don't":  # Match is "don't"
            enable = False
        elif m.group(0) == "do":  # Match is "do"
            enable = True

print(sum)
