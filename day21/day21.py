import sys
import os

# Add the parent directory to sys.path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from progress_bar import progress_bar

# -------- Day 21 --------
def load_keys(file_path):
	with open(file_path, 'r') as file:
		lines = file.readlines()

	# Remove any trailing whitespace or newlines
	keys = [list(line.strip()) for line in lines]

	return keys

file_path = "day21.txt"
keys = load_keys(file_path)

# ----- part 1 -----
print("-------------")
print("Part 1")

import re
def check_string(s):
	num_chars = len(set(s))
	# Check if the string contains at most two distinct characters
	if num_chars > 2:
		return False
	if num_chars > 1:
		# Check if the string has all characters grouped together
		if re.match(r'^([<^>v])\1*([<^>v])?\2*$', s):
			return True
		return False
	return True

def generate_movements():
	# Define the positions of the keys on the keypad
	keypad_arrow = {
		'^': (0, 1),
		'A': (0, 2),
		'<': (1, 0),
		'v': (1, 1),
		'>': (1, 2)
	}
	keypad_arrow_forbidden = (0, 0)

	# Define the positions of the keys on the second keypad
	keypad_code = {
		'7': (0, 0), '8': (0, 1), '9': (0, 2),
		'4': (1, 0), '5': (1, 1), '6': (1, 2),
		'1': (2, 0), '2': (2, 1), '3': (2, 2),
		'0': (3, 1), 'A': (3, 2)
	}
	keypad_code_forbidden = (3, 0)

	def get_arrow_sequence(start, end, forbidden):

		def gen_moves(current_x, current_y, end_x, end_y, invert):
			moves = []
			while (current_x, current_y) != (end_x, end_y):
				if invert:
					if current_x < end_x:
						current_x += 1
						moves.append('v')
					elif current_x > end_x:
						current_x -= 1
						moves.append('^')
					elif current_y < end_y:
						current_y += 1
						moves.append('>')
					elif current_y > end_y:
						current_y -= 1
						moves.append('<')
					if (current_x, current_y) == forbidden:
						return []
				else:
					if current_y < end_y:
						current_y += 1
						moves.append('>')
					elif current_y > end_y:
						current_y -= 1
						moves.append('<')
					elif current_x < end_x:
						current_x += 1
						moves.append('v')
					elif current_x > end_x:
						current_x -= 1
						moves.append('^')
					if (current_x, current_y) == forbidden:
						return []

			return moves

		# Calculate the arrow sequence needed to move from start to end
		moves11 = []
		current_x, current_y = start
		end_x, end_y = end
		invert = False

		moves1 = gen_moves(current_x, current_y, end_x, end_y, True)
		moves2 = gen_moves(current_x, current_y, end_x, end_y, False)


		return ''.join(moves1), ''.join(moves2)

	# Generate all unique movement pairs
	movements_arrow = {}
	for start_key, start_pos in keypad_arrow.items():
		for end_key, end_pos in keypad_arrow.items():
			if start_key != end_key:  # Exclude movements to the same key
				sequence1, sequence2 = get_arrow_sequence(start_pos, end_pos, keypad_arrow_forbidden)
				assert check_string(sequence1), f"sequence of {start_key}@{start_pos} to {end_key}@{end_pos} is {sequence1}"
				assert check_string(sequence2), f"sequence of {start_key}@{start_pos} to {end_key}@{end_pos} is {sequence2}"
				if not ((start_key, end_key) in movements_arrow):
					movements_arrow[(start_key, end_key)] = []
				if len(sequence1) > 0:
					movements_arrow[(start_key, end_key)].append(sequence1)
				if len(sequence2) > 0:
					movements_arrow[(start_key, end_key)].append(sequence2)

	movements_code = {}
	for start_key, start_pos in keypad_code.items():
		for end_key, end_pos in keypad_code.items():
			if start_key != end_key:  # Exclude movements to the same key
				sequence1, sequence2 = get_arrow_sequence(start_pos, end_pos, keypad_code_forbidden)
				assert check_string(sequence1), f"sequence of {start_key}@{start_pos} to {end_key}@{end_pos} is {sequence1}"
				assert check_string(sequence2), f"sequence of {start_key}@{start_pos} to {end_key}@{end_pos} is {sequence2}"
				if not ((start_key, end_key) in movements_code):
					movements_code[(start_key, end_key)] = []
				if len(sequence1) > 0:
					movements_code[(start_key, end_key)].append(sequence1)
				if len(sequence2) > 0:
					movements_code[(start_key, end_key)].append(sequence2)

	return movements_arrow, movements_code

# Generate and print all movements
movement_pairs_arrow, movement_pairs_code = generate_movements()

from functools import cache
@cache
def seq_robot2code(prev, next, ver):
	if prev == next:
		return "A"
	if 0 <= ver < len(movement_pairs_code[(prev, next)]):
		return movement_pairs_code[(prev, next)][ver] + "A"
	return []
@cache
def seq_robot2robot(prev, next, ver):
	if prev == next:
		return "A"
	if 0 <= ver < len(movement_pairs_arrow[(prev, next)]):
		return movement_pairs_arrow[(prev, next)][ver] + "A"
	return []

@cache
def seq_user2robot(prev, next, ver):
	return seq_robot2robot(prev, next, ver)


import itertools
def find_shortest_code_versions(key):
	best_versions = []
	best_length = float('inf')  # Start with a very large number
	import itertools

	# Iterate over all possible extra_argument sequences
	for extra_arguments in itertools.product([0, 1], repeat=len(key)):
		movements_robot2code = []
		previous = "A"
		valid = True
		# Iterate through the key, passing different extra_arguments to seq_robot2code
		for i, next in enumerate(key):
			seq = seq_robot2code(previous, next, extra_arguments[i])
			if len(seq) > 0:
				movements_robot2code.extend(seq_robot2code(previous, next, extra_arguments[i]))
				previous = next
			else:
				valid = False
				break

		if valid:
			# Check if this version has the shortest length
			if len(movements_robot2code) < best_length:
				best_versions = [tuple(movements_robot2code)]  # Reset the list with this new best version
				best_length = len(movements_robot2code)
			elif len(movements_robot2code) == best_length:
				best_versions.append(tuple(movements_robot2code))  # Add this version to the list of best versions


	def remove_duplicates(list_of_lists):
		return list(set(list_of_lists))
	# print(best_versions)
	# Return the best versions joined as strings
	return remove_duplicates(["".join(version) for version in best_versions])

@cache
def explore(key, level):
	# print("==========")
	# print("explore", key, level)
	if level == 25:
		# print("returning", len(key))
		return len(key)

	best = float('inf')
	for extra_arguments in itertools.product([0, 1], repeat=len(key)):
		# print(extra_arguments)
		movements_robot2code = []
		previous = "A"
		total = 0
		valid = True
		# Iterate through the key, passing different extra_arguments to seq_robot2code
		for i, next in enumerate(key):
			seq = seq_robot2robot(previous, next, extra_arguments[i])

			# print(previous, next, "-->", seq, len(seq), "total", total)
			if len(seq) > 0:
				total += explore(seq, level + 1)
			else:
				valid = False
				break
			previous = next
		# print("total", total, valid)
		if valid and total < best:
			# print("updating best", total)
			best = total
	# print("best", best)
	# exit()
	return best

# Wrapper to call the DFS for the shortest versions found earlier, applying seq_robot2robot and seq_user2robot
def process_best_versions_with_dfs(key):
	shortest_versions = find_shortest_code_versions(key)  # Get the best versions first

	# print("Best version:", shortest_versions)
	# Perform a DFS to find the best output after applying seq_robot2robot and seq_user2robot
	best = float('inf')
	for ver in shortest_versions:
		result = explore(ver, 0)
		if result < best:
			best = result

	return best

running_score = 0
for key in keys:
	print(key)
	best_result = process_best_versions_with_dfs(key)
	# print("Best result:", best_result)

	def compute_score(lenght, key):
		print(lenght, int("".join(key[:-1])))
		return lenght * int("".join(key[:-1]))

	score = compute_score(best_result, key)
	running_score += score

	print("".join(key), "Score", score)
	# exit()

print("Running score", running_score)

# ----- part 2 -----
print("-------------")
print("Part 2")

running_score = 0
for key in keys:
	print(key)
	best_result = process_best_versions_with_dfs(key)
	# print("Best result:", best_result)

	def compute_score(lenght, key):
		print(lenght, int("".join(key[:-1])))
		return lenght * int("".join(key[:-1]))

	score = compute_score(best_result, key)
	running_score += score

	print("".join(key), "Score", score)
	# exit()

print("Running score", running_score)
	