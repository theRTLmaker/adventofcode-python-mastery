import sys
import os

# Add the parent directory to sys.path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from progress_bar import progress_bar

# -------- Day 15 --------
def load_patterns(file_path):
	with open(file_path, 'r') as file:
		lines = file.read().strip().split('\n')

	# First list: patterns split by commas
	patterns = [pattern.strip() for pattern in lines[0].split(',')]

	# Second list: combinations (remaining lines after the first line)
	combinations = lines[2:]

	return patterns, combinations

file_path = "day19.txt"
patterns, combinations = load_patterns(file_path)

# Display results
print("Available Patterns:", patterns)
print("Patterns:", combinations)

# ----- part 1 -----
print("-------------")
print("Part 1")

from functools import cache
@cache
def search(word):
	if len(word) == 0:
		return 1

	for pat in patterns:
		if word.startswith(pat):
			search_word = word[len(pat):]
			res = search(search_word)
			if res > 0:
				return res + 1

	return 0


possible_designs = 0
total = len(combinations)
for i, comb in enumerate(combinations):
	progress_bar(i, total)
	res = search(comb)
	if res > 0:
		possible_designs += 1
		# print(comb, "is possible with", res)

print()
print()
print("Possible designs", possible_designs)

# ----- part 2 -----
print("-------------")
print("Part 2")


from functools import cache
@cache
def search_all(word):
	if len(word) == 0:
		return 1

	res = 0
	for pat in patterns:
		if word.startswith(pat):
			search_word = word[len(pat):]
			res += search_all(search_word)

	return res


possible_designs = 0
total = len(combinations)
for i, comb in enumerate(combinations):
	progress_bar(i, total)
	res = search_all(comb)
	if res > 0:
		possible_designs += res
		# print(comb, "is possible with", res)

print()
print()
print("Possible designs", possible_designs)
