import sys
import os

# Add the parent directory to sys.path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from progress_bar import progress_bar

# -------- Day 15 --------

def load_map_and_movements(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Remove any trailing whitespace or newlines
    lines = [line.strip() for line in lines]

    # Find the index of the empty line separating the map and movements
    separator_index = lines.index('')

    # Extract the map
    map_data = lines[:separator_index]
    map_grid = [list(row) for row in map_data]

    # Find the initial position of '@'
    initial_position = None
    for i, row in enumerate(map_grid):
        if '@' in row:
            initial_position = (i, row.index('@'))
            break

    # Extract the movements
    movements = ''.join(lines[separator_index + 1:])

    return map_grid, initial_position, list(movements)

file_path = "day15.txt"
map_grid, initial_position, movements = load_map_and_movements(file_path)

# Display results
print("Map Grid:")
for row in map_grid:
    print(''.join(row))

print("\nMovements:")
print(''.join(movements))

X_len = len(map_grid[0])
Y_len = len(map_grid)

# ----- part 1 -----
print("-------------")
print("Part 1")

pos = initial_position

for mov in movements:
    def compute_new_pos(pos, dir):
        if dir == "^":
            new_pos = (pos[0], pos[1]-1)
        elif dir == "<":
            new_pos = (pos[0]-1, pos[1])
        elif dir == ">":
            new_pos = (pos[0]+1, pos[1])
        else:
            new_pos = (pos[0], pos[1]+1)

        return new_pos

    def apply_move(pos, dir):
        new_pos = compute_new_pos(pos, dir)

        # Check if new pos in map
        if 0 <= new_pos[0] < X_len and 0 <= new_pos[1] < Y_len:

            if map_grid[new_pos[1]][new_pos[0]] == "#":
                # If it found a wall, stop recursion
                return 0
            elif map_grid[new_pos[1]][new_pos[0]] == "O":
                # If it found a another box, check that box
                should_move = apply_move(new_pos, dir)
                if should_move:
                    map_grid[new_pos[1]][new_pos[0]] = map_grid[pos[1]][pos[0]]
                    map_grid[pos[1]][pos[0]] = "."

                    return 1
            else:
                # If it found an empty space, move
                map_grid[new_pos[1]][new_pos[0]] = map_grid[pos[1]][pos[0]]
                map_grid[pos[1]][pos[0]] = "."

                return 1

        return 0

    moved = apply_move(pos, mov)
    if moved:
        pos = compute_new_pos(pos, mov)

# Display results
print("Map Grid:")
for row in map_grid:
    print(''.join(row))

def compute_score():
    score = 0

    for y in range(len(map_grid)):
        for x in range(len(map_grid[y])):
            if map_grid[y][x] == "O":
                score += 100 * y + x

    return score

print("Score", compute_score())
print()
# ----- part 2 -----
print("-------------")
print("Part 2")

map_grid, initial_position, movements = load_map_and_movements(file_path)

def compute_adjusted_map():
    new_map = []
    initial_position = (0, 0)
    for y in range(len(map_grid)):
        new_map.append([])
        for x in range(len(map_grid[y])):
            if map_grid[y][x] == "O":
                new_map[y].extend(["[", "]"])
            elif map_grid[y][x] == "#":
                new_map[y].extend(["#", "#"])
            elif map_grid[y][x] == ".":
                new_map[y].extend([".", "."])
            elif map_grid[y][x] == "@":
                new_map[y].extend(["@", "."])
                initial_position = (len(new_map[y])-2, y)
    return new_map, initial_position

map_grid, initial_position = compute_adjusted_map()
print("New Map Grid:")
for row in map_grid:
    print(''.join(row))

X_len = len(map_grid[0])
Y_len = len(map_grid)

pos = initial_position

for ite, mov in enumerate(movements):
    def compute_new_pos(pos, dir):
        if dir == "^":
            new_pos = (pos[0], pos[1]-1)
        elif dir == "<":
            new_pos = (pos[0]-1, pos[1])
        elif dir == ">":
            new_pos = (pos[0]+1, pos[1])
        else:
            new_pos = (pos[0], pos[1]+1)

        return new_pos

    def can_move(pos, dir):
        new_pos = compute_new_pos(pos, dir)

        # Check if new pos in map
        if 0 <= new_pos[0] < X_len and 0 <= new_pos[1] < Y_len:
            obj = map_grid[new_pos[1]][new_pos[0]]
            # print(obj)
            if obj == "#":
                # If it found a wall, stop recursion
                return 0
            elif obj in ["[", "]"]:
                if dir == "<" or dir == ">":
                    # If it found a another box, check that box
                    if can_move(new_pos, dir):
                        return 1
                else:
                    if obj == "[":
                        other_new_pos = (new_pos[0]+1, new_pos[1])
                        other_pos = (pos[0]+1, pos[1])
                    else:
                        other_new_pos = (new_pos[0]-1, new_pos[1])
                        other_pos = (pos[0]-1, pos[1])

                    # If it found a another box, check that box
                    should_move1 = can_move(new_pos, dir)
                    should_move2 = can_move(other_new_pos, dir)

                    if should_move1 and should_move2:
                        return 1

            else:
                return 1
        print("Can't move", pos, new_pos)
        return 0

    def apply_move(pos, dir):
        new_pos = compute_new_pos(pos, dir)

        # Check if new pos in map
        if 0 <= new_pos[0] < X_len and 0 <= new_pos[1] < Y_len:
            obj = map_grid[new_pos[1]][new_pos[0]]
            # print(obj)
            if obj == "#":
                # If it found a wall, stop recursion
                return
            elif obj in ["[", "]"]:
                if dir == "<" or dir == ">":
                    # If it found a another box, check that box
                    should_move = apply_move(new_pos, dir)
                    if should_move:
                        map_grid[new_pos[1]][new_pos[0]] = map_grid[pos[1]][pos[0]]
                        map_grid[pos[1]][pos[0]] = "."

                        return 1
                else:
                    if obj == "[":
                        other_new_pos = (new_pos[0]+1, new_pos[1])
                        other_pos = (pos[0]+1, pos[1])
                    else:
                        other_new_pos = (new_pos[0]-1, new_pos[1])
                        other_pos = (pos[0]-1, pos[1])

                    # If it found a another box, check that box
                    should_move1 = apply_move(new_pos, dir)
                    should_move2 = apply_move(other_new_pos, dir)
                    # if map_grid[pos[1]][pos[0]] == "@":
                    # print()
                    # print(map_grid[new_pos[1]][new_pos[0]], ":", new_pos, should_move1, dir)
                    # print(map_grid[other_new_pos[1]][other_new_pos[0]], ":", other_new_pos, should_move2, dir)
                    if should_move1 and should_move2:
                        map_grid[new_pos[1]][new_pos[0]] = map_grid[pos[1]][pos[0]]
                        map_grid[pos[1]][pos[0]] = "."
                        if map_grid[other_new_pos[1]][other_new_pos[0]] in ["[", "]"]:
                            map_grid[other_new_pos[1]][other_new_pos[0]] = map_grid[other_pos[1]][other_pos[0]]
                            map_grid[other_pos[1]][other_pos[0]] = "."
                        return 1

            else:
                map_grid[new_pos[1]][new_pos[0]] = map_grid[pos[1]][pos[0]]
                map_grid[pos[1]][pos[0]] = "."

                return 1

    print("-------------")
    print("Iteration", ite, mov)

    moved = can_move(pos, mov)
    if moved:
        print("Moved")
        apply_move(pos, mov)
        pos = compute_new_pos(pos, mov)



    # Display results
    # print("Map Grid:")
    # print(" ", "".join(list(map(str, range(len(map_grid[0])-1)))))
    # for y, row in enumerate(map_grid):
    #     print(y, ''.join(row))

    # if ite > 10:
    #     break



def compute_score():
    score = 0

    for y in range(len(map_grid)):
        for x in range(len(map_grid[y])):
            if map_grid[y][x] == "[":
                score += 100 * y + x

    return score

print("Score", compute_score())
print()