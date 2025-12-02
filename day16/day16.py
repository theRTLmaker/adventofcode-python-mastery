import sys
import os

# Add the parent directory to sys.path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from progress_bar import progress_bar

# -------- Day 15 --------
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
			break
		if 'E' in row:
			end_position = (i, row.index('E'))

		if initial_position and end_position:
			break


	return map_grid, initial_position, end_position

file_path = "day16.txt"
map_grid, initial_position, end_position = load_map(file_path)

# Display results
print("Map Grid:")
for row in map_grid:
	print(''.join(row))

print("Starting position:", initial_position)
print("Target position:", end_position)

# ----- part 1 -----
print("-------------")
print("Part 1")

def print_debug_matrix(matrix, distances):
	"""Visualize the distances matrix with aligned columns."""
	align = 5
	row_info = []
	for i in range(len(matrix[0])):
		row_info.append(f"{i:>{align}}")
	print("", " ".join(row_info))

	for i, row in enumerate(matrix):
		row_info = []
		for j, cell in enumerate(row):
			if cell == '#':
				row_info.append(f"{'#':>{align}}")
			else:
				min_cost = min(distances[i][j])
				if min_cost == float('inf'):
					row_info.append(f"{'.':>{align}}")
				else:
					row_info.append(f"{min_cost:>5}")
					# row_info.append(f"{min_cost}")
		print(f"{i:>2}", " ".join(row_info))
	print()

import heapq

def shortest_path_with_locked_directions(matrix, start, end, turning_cost):
	rows, cols = len(matrix), len(matrix[0])
	directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up
	distances = [[[float('inf')] * len(directions) for _ in range(cols)] for _ in range(rows)]

	# Priority queue: (distance, row, col, direction)
	pq = []
	# Start with the initial orientation facing East (index 0)
	initial_direction = 0
	heapq.heappush(pq, (0, start[0], start[1], initial_direction))
	distances[start[0]][start[1]][initial_direction] = 0


	while pq:
		current_distance, x, y, direction = heapq.heappop(pq)

		if (x, y) == end:
			print_debug_matrix(matrix, distances)
			return current_distance, distances  # Stop when reaching the target

		# Move forward
		dx, dy = directions[direction]
		nx, ny = x + dx, y + dy
		if 0 <= nx < rows and 0 <= ny < cols and matrix[nx][ny] in ['.', "E"]:
			new_distance = current_distance + 1
			if new_distance < distances[nx][ny][direction]:
				distances[nx][ny][direction] = new_distance
				heapq.heappush(pq, (new_distance, nx, ny, direction))

		# Turn and move
		for new_direction, (dx, dy) in enumerate(directions):
			if new_direction != direction:
				nx, ny = x + dx, y + dy
				if 0 <= nx < rows and 0 <= ny < cols and matrix[nx][ny] in ['.', "E"]:
					new_distance = current_distance + turning_cost + 1
					if new_distance < distances[nx][ny][new_direction]:
						distances[nx][ny][new_direction] = new_distance
						heapq.heappush(pq, (new_distance, nx, ny, new_direction))

	return -1, distances  # Return -1 if the target is unreachable


turning_cost = 1000
cost, distances = shortest_path_with_locked_directions(map_grid, initial_position, end_position,  turning_cost)
print(cost)

print("Starting position:", initial_position)
print("Target position:", end_position)

# ----- part 2 -----
print("-------------")
print("Part 2")

turning_cost = 1000
cost, distances = shortest_path_with_locked_directions(map_grid, initial_position, end_position,  turning_cost)

def count_cells_on_all_shortest_paths(matrix, start, end, distances, turning_cost):
	rows, cols = len(matrix), len(matrix[0])
	directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up
	path_cells = set()

	def print_visited_matrix():
		import copy
		vis_matrix = copy.deepcopy(matrix)
		for cell in path_cells:
			vis_matrix[cell[0]][cell[1]] = True

		for i, row in enumerate(vis_matrix):
			row_info = []
			for j, cell in enumerate(row):
				if cell == True:
					row_info.append("X")
				else:
					row_info.append(cell)
			print(f"{i:>2}", " ".join(row_info))

	def backtrack(x, y, current_cost, current_direction):
		# print()
		# print((x, y), min(distances[x][y]))
		if (x, y) == start:
			path_cells.add((x, y))
			return

		path_cells.add((x, y))

		for new_direction, (dx, dy) in enumerate(directions):
			nx, ny = x - dx, y - dy  # Reverse direction (backtracking)
			rev_direction = (new_direction + 2) % 4
			# print("Checking:", (nx, ny), distances[nx][ny])
			# print("->", new_direction, (nx, ny), distances[nx][ny][new_direction])
			# Ensure we are within bounds and the cell is valid
			if 0 <= nx < rows and 0 <= ny < cols:
				for check_directions in range(len(directions)):
					if distances[nx][ny][check_directions] != float('inf'):
						# Calculate the cost to move from (nx, ny) to (x, y)
						move_cost = 1
						turn_cost = turning_cost if check_directions != current_direction else 0
						total_cost = move_cost + turn_cost


						# print("Aim to:", distances[nx][ny][check_directions], rev_direction)
						# print("Searching", (nx, ny), total_cost, distances[nx][ny][check_directions] + total_cost, current_cost)

						# Check if this direction and position were part of a shortest path
						if distances[nx][ny][check_directions] + total_cost <= current_cost:
							# Backtrack recursively in all directions that give the same optimal cost
							backtrack(nx, ny, distances[nx][ny][check_directions], check_directions)

	# Start backtracking from the end position for all directions
	min_distance_to_end = min(distances[end[0]][end[1]])

	# Explore all directions leading to the minimum cost at the end position
	for direction, distance in enumerate(distances[end[0]][end[1]]):
		if distance == min_distance_to_end:
			backtrack(end[0], end[1], distance, direction)

	# print_visited_matrix()

	return len(path_cells)

# print(distances[7][5])
print(count_cells_on_all_shortest_paths(map_grid, initial_position, end_position, distances, turning_cost))
# print_debug_matrix(map_grid, distances)


