# -------- Day 6 --------
# part 1
import time

map = []

with open("day6.txt", "r") as f:
  for line in f:
    map.append(list(line.strip()))


def print_map(map):
  for row in map:
    print(" ".join(row))


print_map(map)

from enum import Enum


class Direction(Enum):
  UP = "up"
  DOWN = "down"
  LEFT = "left"
  RIGHT = "right"

  def __str__(self):
    return self.value


class Guard:

  def __init__(self, init_x: int, init_y, init_dir: Direction):
    self.init_x = init_x
    self.init_y = init_y
    self.init_dir = init_dir
    self.reset()

  def reset(self):
    self.x = self.init_x
    self.y = self.init_y
    self.dir = self.init_dir

    self.in_map = True
    self.in_loop = False
    # Create dir_map with the same size as map
    self.dir_map = [[[] for _ in row] for row in map]

  def __repr__(self):
    return f"Guard(x={self.x}, y={self.y}, dir={self.dir})"

  def toggle_dir(self):
    if self.dir == Direction.UP:
      self.dir = Direction.RIGHT
    elif self.dir == Direction.RIGHT:
      self.dir = Direction.DOWN
    elif self.dir == Direction.DOWN:
      self.dir = Direction.LEFT
    else:
      self.dir = Direction.UP

  def commute(self, map):
    while True:
      searching_pos = (self.x, self.y)
      if self.dir == Direction.UP:
        searching_pos = (self.x, self.y - 1)
      elif self.dir == Direction.DOWN:
        searching_pos = (self.x, self.y + 1)
      elif self.dir == Direction.LEFT:
        searching_pos = (self.x - 1, self.y)
      elif self.dir == Direction.RIGHT:
        searching_pos = (self.x + 1, self.y)

      # search if out of bound, if so problem solved
      if searching_pos[0] < 0 or searching_pos[0] >= len(
          map) or searching_pos[1] < 0 or searching_pos[1] >= len(
              map[searching_pos[0]]):
        self.in_map = False
        map[self.y][self.x] = "X"
        break

      if self.detect_loop():
        break

      # print(searching_pos)
      if map[searching_pos[1]][searching_pos[0]] == "#" or map[
          searching_pos[1]][searching_pos[0]] == "O":
        # Change dir
        self.toggle_dir()
        # Stop iterating
        break
      elif map[searching_pos[1]][searching_pos[0]] == "." or map[
          searching_pos[1]][searching_pos[0]] == "X":
        # Place an X on matrix
        map[self.y][self.x] = "X"
        # Update guard new coordinates
        self.x = searching_pos[0]
        self.y = searching_pos[1]

        # Continue
    return

  # Return 1 when a loop is dected: when we are passing a second time
  # with the same direction on the same position
  def detect_loop(self):
    # Check if the current direction already exists in the current position
    if self.dir in self.dir_map[self.y][self.x]:
      self.in_loop = True
      return 1  # Loop detected
    self.dir_map[self.y][self.x].append(self.dir)
    return 0


def find_char_index(char):
  global map
  for row_index, row in enumerate(map):
    for col_index, element in enumerate(row):
      if element == char:
        return (row_index, col_index)  # Return the first match
  return None  # If the character is not found


def get_initial_state():
  global map
  direction_map = {
      "^": Direction.UP,
      "v": Direction.DOWN,
      "<": Direction.LEFT,
      ">": Direction.RIGHT
  }

  # Look for any of the direction markers in the map
  for dir_symbol, dir_enum in direction_map.items():
    position = find_char_index(dir_symbol)
    if position:
      y, x = position
      return Guard(x, y, dir_enum)

  raise ValueError("No initial state found in the map.")


def count_character(char, map):
  count = sum(row.count(char) for row in map)
  print(f"Total '{char}' in the map: {count}")


guard = get_initial_state()
print(guard)

iteration = 0
while guard.in_map:
  # print(iteration)
  guard.commute(map)
  # if iteration % 100 == 0:
  #   print_map(map)
  iteration += 1
  # time.sleep(0.5)

print_map(map)
count_character("X", map)
# get initial posi
# run_game
# use direction and compute target cell/output
# update map with

# ---- part 2 ----
map = []

with open("day6.txt", "r") as f:
  for line in f:
    map.append(list(line.strip()))

import copy

guard = get_initial_state()
loop_positions_found = 0
for x in range(len(map)):
  for y in range(len(map[x])):
    if map[x][y] == ".":
      new_map = copy.deepcopy(map)
      # Place the new obstacle
      new_map[x][y] = "O"
      guard.reset()

      while guard.in_map:
        guard.commute(new_map)
        iteration += 1

        if guard.in_loop:
          print("----loop found-----", loop_positions_found)
          # print_map(new_map)
          loop_positions_found += 1
          break

print("loop_positions_found:", loop_positions_found)
