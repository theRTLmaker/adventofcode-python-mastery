import sys
import os

# Add the parent directory to sys.path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from progress_bar import progress_bar

# -------- Day 23 --------
import re

def extract_matching_pairs(file_path):
	"""
	Extract lines from a file that match the pattern: two lowercase letters, a hyphen, and two lowercase letters.

	Args:
		file_path (str): Path to the file.

	Returns:
		list: List of matching pairs as strings.
	"""
	# Define the regex pattern
	pattern = re.compile(r'^([a-z]{2})-([a-z]{2})$')

	matching_tuples = []

	# Read the file and filter matching lines
	with open(file_path, "r") as file:
		for line in file:
			match = pattern.match(line.strip())
			if match:
				# Extract groups and append as a tuple
				matching_tuples.append((match.group(1), match.group(2)))

	return matching_tuples


file_path = "day23.txt"
connections = extract_matching_pairs(file_path)

# ----- part 1 -----
print("-------------")
print("Part 1")

def build_adjency_list(connections):
	adj_list = {}
	for v1, v2 in connections:
		if v1 in adj_list:
			adj_list[v1].append(v2)
		else:
			adj_list[v1] = [v2]

		if v2 in adj_list:
			adj_list[v2].append(v1)
		else:
			adj_list[v2] = [v1]

	return adj_list

adj_list = build_adjency_list(connections)

def count_triangles(adj_list):
	count = 0
	for v1 in adj_list.keys():
		for v2 in adj_list[v1]:
			# Only proceed if v2 > v1 to avoid duplicate counting
			if v2 > v1:
				for v3 in adj_list[v1]:
					# Ensure v3 > v2 to maintain order and avoid duplicates
					if v3 > v2 and v3 in adj_list[v2]:
						if v1.startswith("t") or v2.startswith("t") or v3.startswith("t"):
							count += 1

	return count

count = count_triangles(adj_list)

print(f"The number of found triangles is {count}")

# ----- part 2 -----
print("-------------")
print("Part 2")

def find_biggest_lan(adj_list):
	nodes = list(adj_list.keys())
	n = len(nodes)
	biggest_lan = []

	# Find the biggest subset of nodes that all belong together
	def backtracking(subset, start_node):
		nonlocal biggest_lan

		if len(subset) > len(biggest_lan):
			biggest_lan = subset[:]

		for i in range(start_node, n):
			next_node = nodes[i]
			# Check if the next node is connected to all the nodes currently in the subset
			if all(next_node in adj_list[node] for node in subset):
				subset.append(next_node)
				backtracking(subset, i + 1)
				subset.pop()


	backtracking([], 0)

	return biggest_lan


adj_list = build_adjency_list(connections)
max_clique = find_biggest_lan(adj_list)

password = ",".join(sorted(max_clique))

print(f"The maximum lan party is {max_clique}")
print(f"The password is {password}")
