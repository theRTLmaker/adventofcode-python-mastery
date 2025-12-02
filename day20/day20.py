import sys
import os

# Add the parent directory to sys.path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from progress_bar import progress_bar

# -------- Day 20 --------
def load_map(file_path):
	with open(file_path, 'r') as file:
		lines = file.readlines()

	# Remove any trailing whitespace or newlines
	map_data = [line.strip() for line in lines]

	# Extract the map
	map_grid = [list(row) for row in map_data]

	# Find the initial and end position
	initial_position = None
	end_position = None
	for i, row in enumerate(map_grid):
		if 'S' in row:
			initial_position = (i, row.index('S'))

		if 'E' in row:
			end_position = (i, row.index('E'))

	return map_grid, initial_position, end_position

def print_map(map):
	"""Visualize the map matrix with aligned columns."""
	row_info = []
	for i in range(len(map[0])):
		row_info.append(str(i))
	print("  ", " ".join(row_info))

	for i, row in enumerate(map):
		print(f"{i:>2}", " ".join(row))
	print()

file_path = "day20.txt"
map, initial_position, end_position = load_map(file_path)

# Display results
# print_map(map)

print("Starting position:", initial_position)
print("Target position:", end_position)

# ----- part 1 -----
print("-------------")
print("Part 1")

def print_debug_matrix(matrix):
	"""Visualize the memory matrix with aligned columns."""
	align = 5
	row_info = []
	for i in range(len(matrix[0])):
		row_info.append(str(i))
	print("  ", "  ".join(row_info))

	for i, row in enumerate(matrix):
		# print(f"{i:>0}", "  ".join(row))
		print(row)
	print()

import heapq

def dijkstra(matrix, start, end):
	rows, cols = len(matrix), len(matrix[0])

	# Initialize distances with infinity
	distances = [[float('inf')] * cols for _ in range(rows)]
	distances[start[0]][start[1]] = 0

	# To reconstruct the path
	parents = {}

	# Priority queue for Dijkstra's algorithm
	pq = [(0, start)]  # (distance, (x, y))

	# Directions for moving in the grid
	directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

	while pq:
		current_distance, (x, y) = heapq.heappop(pq)

		# If we reach the end, return the result
		if (x, y) == end:
			# Backtrack to find the path
			path = []
			current = end
			while current:
				path.append(current)
				current = parents.get(current)
			path.reverse()
			return distances[x][y], path

		# If current distance is greater than recorded, skip
		if current_distance > distances[x][y]:
			continue

		# Explore neighbors
		for dx, dy in directions:
			nx, ny = x + dx, y + dy
			if 0 <= nx < rows and 0 <= ny < cols and matrix[nx][ny] in ['.', 'E']:
				new_distance = current_distance + 1
				if new_distance < distances[nx][ny]:
					distances[nx][ny] = new_distance
					parents[(nx, ny)] = (x, y)
					heapq.heappush(pq, (new_distance, (nx, ny)))

	# Reconstruct path
	path = []
	node = end
	while node is not None:
		path.append(node)
		node = parents[node]
	path.reverse()

	# If the end is unreachable, return infinity
	return float('inf'), []


baseline_timespent, path = dijkstra(map, initial_position, end_position)

print("Starting position:", initial_position)
print("Target position:", end_position)
print("Baseline Time:", baseline_timespent)
# print("Path:", path)

def is_passable_wall(matrix, coord, direction):
	rows, cols = len(matrix), len(matrix[0])
	x, y = coord

	# Ensure the coordinate is within the map
	if not (0 <= x < rows and 0 <= y < cols):
		return False

	# Check if the coordinate is a wall
	if matrix[x][y] != '#':
		return False

	dx, dy = direction
	nx, ny = x + dx, y + dy

	# Check if the neighboring cell is within bounds
	if 0 <= nx < rows and 0 <= ny < cols:
		if matrix[nx][ny] in ['.', 'S', 'E']:  # Non-wall on one side
			return True

	return False

cheats = []
tested_cheats = set()

# Directions for checking the "other side" of the wall
directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
total = len(path)
for ite, entry in enumerate(path):
	progress_bar(ite, total)
	for dir in directions:
		coord = (entry[0] + dir[0], entry[1] + dir[1])
		if not (coord in tested_cheats):
			# print(coord, dir)
			if is_passable_wall(map, coord, dir):
				prev_data = map[coord[0]][coord[1]]
				map[coord[0]][coord[1]] = "."
				timespent, _ = dijkstra(map, initial_position, end_position)
				# print("Yes", timespent)
				if timespent < baseline_timespent - 99:
					cheats.append([coord, baseline_timespent - timespent])
				map[coord[0]][coord[1]] = prev_data
			tested_cheats.add(coord)


print("Num cheats", len(cheats))

# ----- part 2 -----
print("-------------")
print("Part 2")

from itertools import combinations

# Generate all possible pairs
index_generator = ((i, j) for i, j in combinations(range(len(path)), 2))
cheats_found = 0
# Analyze pairs directly from the generator
for i, j in index_generator:
	progress_bar(i, baseline_timespent)
	def compute_euclidian_dist(coord1, coord2):
		return abs(coord1[0]-coord2[0])+abs(coord1[1]-coord2[1])
	dist = compute_euclidian_dist(path[i], path[j])
	if dist <= 20:
		if baseline_timespent - (j - i) + dist <= baseline_timespent - 100:
			cheats_found += 1

print()
print()
print("Starting position:", initial_position)
print("Target position:", end_position)
print("Cheats found:", cheats_found)