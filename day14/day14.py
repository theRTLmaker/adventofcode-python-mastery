import sys
import os

# Add the parent directory to sys.path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from progress_bar import progress_bar

# -------- Day 13 --------

import re
# Pattern to match Button and Prize values
pattern = r"p=([\d-]+),([\d-]+)\s+v=([\d-]+),([\d-]+)"

# Read the input from the file
with open("day14.txt", "r") as file:
	data = file.read()

# Find all matches in the input string
matches = re.findall(pattern, data)

# Process each match and convert to integers
robots = []
for match in matches:
    coordinates = (int(match[0]), int(match[1]))
    velocities = (int(match[2]), int(match[3]))
    robots.append({
         "coordinates": coordinates,
         "velocities": velocities})

def print_matrix(matrix):
    for row in matrix:
        formatted_row = "".join(str(cell) if cell != 0 else '.' for cell in row)
        print(formatted_row)

X_len = 101
Y_len = 103

# ----- part 1 -----
print("Part 1")
iterations = 100

representation = [[0 for x in range(X_len)] for y in range(Y_len)]

for robot in robots:
    print(f"Coordinates: {robot['coordinates']}, Velocities: {robot['velocities']}")
    print(f"Coordinates: {robot['coordinates']}")
    end_position_x = (robot['coordinates'][0] + iterations * robot['velocities'][0]) % X_len
    end_position_y = (robot['coordinates'][1] + iterations * robot['velocities'][1]) % Y_len
    robot["end_pos"] = (end_position_x, end_position_y)
    representation[end_position_y][end_position_x] += 1

print_matrix(representation)

half_X_len = X_len // 2
half_Y_len = Y_len // 2

quadrants_count = 4 * [0]
for robot in robots:
    x = robot["end_pos"][0]
    y = robot["end_pos"][1]
    if x < half_X_len and y < half_Y_len:
        quadrants_count[0] += 1
    elif x < half_X_len and y > half_Y_len:
        quadrants_count[2] += 1
    elif x > half_X_len and y < half_Y_len:
        quadrants_count[1] += 1
    elif x > half_X_len and y > half_Y_len:
        quadrants_count[3] += 1

print("quadrants_count", quadrants_count)
from functools import reduce
from operator import mul
print("quadrants_count", reduce(mul, quadrants_count))

# ----- part 2 -----
print("Part 2")

# ....1.... = 1
# ...111... = 3
# ..11111.. = 5
# .1111111. = 7
# 111111111 = 9
# ..1111111 = 9

representation = [[0 for x in range(X_len)] for y in range(Y_len)]

for i in range(10000):
    for robot in robots:
        end_position_x = (robot['coordinates'][0] + i * robot['velocities'][0]) % X_len
        end_position_y = (robot['coordinates'][1] + i * robot['velocities'][1]) % Y_len
        if i > 0:
            representation[robot["end_pos"][1]][robot["end_pos"][0]] -= 1
        robot["end_pos"] = (end_position_x, end_position_y)
        representation[robot["end_pos"][1]][robot["end_pos"][0]] += 1

    def has_large_cluster(matrix, min_size=15):
        def dfs(x, y):
            # Check bounds and value > 0
            if x < 0 or y < 0 or x >= rows or y >= cols or matrix[x][y] <= 0 or visited[x][y]:
                return 0
            # Mark the cell as visited
            visited[x][y] = True
            size = 1  # Count current cell
            # Explore all 8 possible directions
            for dx, dy in directions:
                size += dfs(x + dx, y + dy)
            return size

        if not matrix:
            return False

        rows, cols = len(matrix), len(matrix[0])
        visited = [[False for _ in range(cols)] for _ in range(rows)]
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1),  # up, down, left, right
                    (-1, -1), (-1, 1), (1, -1), (1, 1)]  # diagonals

        for x in range(rows):
            for y in range(cols):
                if matrix[x][y] > 0 and not visited[x][y]:
                    cluster_size = dfs(x, y)
                    if cluster_size >= min_size:
                        return True  # Found a cluster large enough

        return False  # No cluster with required size found

    # if i % 1000:
    #     print("-------------")
    #     print("-------------")
    #     print("-------------")
    #     print("-------------")
    #     print("-------------")
    #     print_matrix(representation)
    #     break
    if has_large_cluster(representation, 30):
        print("-------------")
        print("-------------")
        print("FOUND")
        print("-------------")
        print("-------------")
        print_matrix(representation)
        print("FOUND", i)
        break

print("END")
