import sys
import os

# Add the parent directory to sys.path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from progress_bar import progress_bar

# -------- Day 13 --------

import re
# Pattern to match Button and Prize values
button_pattern = r"Button [AB]: X\+(\d+), Y\+(\d+)"
prize_pattern = r"Prize: X=(\d+), Y=(\d+)"

# Read the input from the file
with open("day13.txt", "r") as file:
	data = file.read()

# Extract matches
button_matches = re.findall(button_pattern, data)
prize_matches = re.findall(prize_pattern, data)

# Organize the data
results = []
prize_index = 0
for i in range(0, len(button_matches), 2):  # Two button matches per group
	button_a = button_matches[i]
	button_b = button_matches[i + 1]
	prize = prize_matches[prize_index]
	prize_index += 1
	results.append({
		"Button A": {"X": int(button_a[0]), "Y": int(button_a[1])},
		"Button B": {"X": int(button_b[0]), "Y": int(button_b[1])},
		"Prize": {"X": int(prize[0]), "Y": int(prize[1])},
	})

# Print the results
# for i, result in enumerate(results):
#     print(f"Set {i + 1}:")
#     print(f"  Button A: X+{result['Button A']['X']}, Y+{result['Button A']['Y']}")
#     print(f"  Button B: X+{result['Button B']['X']}, Y+{result['Button B']['Y']}")
#     print(f"  Prize: X={result['Prize']['X']}, Y={result['Prize']['Y']}")

# ----- part 1 -----
print("Part 1")

total = len(results)

total_tokens = 0

for i, result in enumerate(results):
	b = (result['Button A']['X']*result["Prize"]['Y']-result['Button A']['Y']*result["Prize"]['X'])/(result['Button A']['X']*result["Button B"]['Y']-result['Button B']['X']*result["Button A"]['Y'])
	a = (result["Prize"]['X']-result["Button B"]['X']*b)/result['Button A']['X']

	if a.is_integer() and b.is_integer():
		total_tokens += 3*int(a) + int(b)

	progress_bar(i, total)

print()
print("Total tokens used:", total_tokens)

# ----- part 2 -----
print("Part 2")

total_tokens = 0

for i, result in enumerate(results):
	result["Prize"]['X'] += 10000000000000
	result["Prize"]['Y'] += 10000000000000

for i, result in enumerate(results):
	b = (result['Button A']['X']*result["Prize"]['Y']-result['Button A']['Y']*result["Prize"]['X'])/(result['Button A']['X']*result["Button B"]['Y']-result['Button B']['X']*result["Button A"]['Y'])
	a = (result["Prize"]['X']-result["Button B"]['X']*b)/result['Button A']['X']

	if a.is_integer() and b.is_integer():
		total_tokens += 3*int(a) + int(b)

	progress_bar(i, total)

print()
print("Total tokens used:", total_tokens)