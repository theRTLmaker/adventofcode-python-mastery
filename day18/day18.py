import sys
import os

# Add the parent directory to sys.path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from progress_bar import progress_bar

# -------- Day 18 --------
def load_bytes(file_path):
	with open(file_path, 'r') as file:
		lines = file.readlines()

	# Remove any trailing whitespace or newlines
	bytes_raw = [line.strip() for line in lines]

	# Extract the map
	bytes_data = [tuple(map(int, byte_entry.split(","))) for byte_entry in bytes_raw]

	return bytes_data

file_path = "day18.txt"
bytes = load_bytes(file_path)

# Display results
# print("Bytes:", bytes)

initial_position = (0,0)
end_position = (70,70)

memory = [["." for _ in range(end_position[0]+1)] for _ in range(end_position[1]+1)]

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
		print(f"{i:>2}", "  ".join(row))
	print()

import heapq

def dijkstra(matrix, start, end):
    rows, cols = len(matrix), len(matrix[0])

    # Initialize distances with infinity
    distances = [[float('inf')] * cols for _ in range(rows)]
    distances[start[0]][start[1]] = 0

    # Priority queue for Dijkstra's algorithm
    pq = [(0, start)]  # (distance, (x, y))

    # Directions for moving in the grid
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while pq:
        current_distance, (x, y) = heapq.heappop(pq)

        # If we reach the end, return the result
        if (x, y) == end:
            return distances, distances[x][y]

        # If current distance is greater than recorded, skip
        if current_distance > distances[x][y]:
            continue

        # Explore neighbors
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols and matrix[nx][ny] == '.':
                new_distance = current_distance + 1
                if new_distance < distances[nx][ny]:
                    distances[nx][ny] = new_distance
                    heapq.heappush(pq, (new_distance, (nx, ny)))

    # If the end is unreachable, return infinity
    return distances, float('inf')

end_ite = 1024


for i, (x, y) in enumerate(bytes):
	memory[y][x] = "#"
	if i >= end_ite - 1:
		break

# print_debug_matrix(memory)

distances, cost = dijkstra(memory, initial_position, end_position)

print("Starting position:", initial_position)
print("Target position:", end_position)
print("Cost:", cost)

# ----- part 2 -----
print("-------------")
print("Part 2")

memory = [["." for _ in range(end_position[0]+1)] for _ in range(end_position[1]+1)]

total = len(bytes)
for i, (x, y) in enumerate(bytes):
	progress_bar(i, total)
	memory[y][x] = "#"
	if i > 1023:
		_, cost = dijkstra(memory, initial_position, end_position)
		if cost == float('inf'):
			print()
			print()

			# print_debug_matrix(memory)
			print(f"Corrupted byte: {i} @({x},{y})")
			break
