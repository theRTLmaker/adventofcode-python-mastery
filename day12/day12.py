import sys
import os

# Add the parent directory to sys.path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from progress_bar import progress_bar

# -------- Day 12 --------
# ----- part 1 -----
print("Part 1")
map=[]
with open('day12.txt', 'r') as file:
  # Read all lines from the file
  for lines in file:
    map_tmp = list(lines.strip())
    map.append(map_tmp)

class Garden_part1:
  def __init__(self, grid):
    self.score = 0
    self.grid = grid
    self.visited_pos = [[False for x in range(len(grid[0]))] for y in range(len(grid))]
    self.perim = 0
    self.area  = 0
    self.directions = ((0, 1), (1, 0), (0, -1), (-1, 0)) # Right, Down, Left, Up
    up_fence = []
    down_fence = []

  def rst(self):
    self.perim = 0
    self.area  = 0
    up_fence = [(0,0),(1,0),(3,0),(4,0), (3,1),(4,1), (2,0)]
    down_fence = [(0,0),(1,0),(3,0),(4,0), (3,1),(4,1), (2,0)]


  def explore(self, position=None):
    """
    Recursive function to explore the grid in all directions.
    :param grid: 2D list representing the grid
    :param position: Current position (row, col) as a tuple
    """
    curr_cluster = self.grid[position[0]][position[1]]

    self.area += 1
    self.visited_pos[position[0]][position[1]] = True
    for direction in self.directions:
        next_pos = (position[0] + direction[0], position[1] + direction[1])

        # If the next position is out of bounds
        if next_pos[0] < 0 or next_pos[1] < 0 or next_pos[0] >= len(self.grid) or next_pos[1] >= len(self.grid[0]):
            self.perim += 1
        elif curr_cluster != self.grid[next_pos[0]][next_pos[1]]:
            self.perim += 1
        elif not self.visited_pos[next_pos[0]][next_pos[1]]:
            self.explore(next_pos)     # Recursive call

  def compute_score(self):
    return self.area * self.perim

total_fence = 0
garden = Garden_part1(map)
for y, map_line in enumerate(map):
  for x in range(len(map_line)):
    garden.rst()
    if not garden.visited_pos[y][x]:
      garden.explore((y,x))
      total_fence += garden.compute_score()

print("Total fence:",  total_fence)

# -------- Day 12 --------
# ----- part 2 -----
print("Part 2")

map=[]
with open('day12.txt', 'r') as file:
  # Read all lines from the file
  for lines in file:
    map_tmp = list(lines.strip())
    map.append(map_tmp)


class Garden_part2:
  def __init__(self, grid):
    self.score = 0
    self.grid = grid
    self.visited_pos = [[False for x in range(len(grid[0]))] for y in range(len(grid))]
    self.area  = 0
    self.directions = ((0, 1), (1, 0), (0, -1), (-1, 0)) # Right, Down, Left, Up
    self.fences = {}
    for dir in self.directions:
        self.fences[dir] = []

  def rst(self):
    self.area  = 0
    for dir in self.directions:
        self.fences[dir] = []

  def explore(self, position=None):
    """
    Recursive function to explore the grid in all directions.
    :param grid: 2D list representing the grid
    :param position: Current position (row, col) as a tuple
    """
    curr_cluster = self.grid[position[0]][position[1]]

    self.area += 1
    self.visited_pos[position[0]][position[1]] = True
    for direction in self.directions:
        next_pos = (position[0] + direction[0], position[1] + direction[1])

        # If the next position is out of bounds
        if next_pos[0] < 0 or next_pos[1] < 0 or next_pos[0] >= len(self.grid) or next_pos[1] >= len(self.grid[0]) or \
            curr_cluster != self.grid[next_pos[0]][next_pos[1]]:
            self.fences[direction].append(next_pos)
        elif not self.visited_pos[next_pos[0]][next_pos[1]]:
            self.explore(next_pos)     # Recursive call

  def compute_fences(self):
    total_fence = 0
    for dir in self.directions:
        total_fence += self.count_fences(self.fences[dir])

    return total_fence

  # Function to find all neighbors of a given coordinate
  def get_neighbors(self, coord, fence_set):
    y, x = coord
    neighbors = [(y + dy, x + dx) for dy, dx in self.directions]
    return [neighbor for neighbor in neighbors if neighbor in fence_set]

  # Count connected components using DFS
  def count_fences(self, fences):
    fence_set = set(fences)  # Convert to set for fast lookup
    visited = set()  # Keep track of visited coordinates
    fence_count = 0

    def dfs(coord):
      stack = [coord]
      while stack:
        current = stack.pop()
        if current not in visited:
          visited.add(current)
          stack.extend(self.get_neighbors(current, fence_set))

    for coord in fences:
      if coord not in visited:
        fence_count += 1
        dfs(coord)  # Explore this new "fence"

    return fence_count

  def compute_score(self):
    return self.area * self.compute_fences()

total_fence = 0
garden = Garden_part2(map)
for y, map_line in enumerate(map):
  for x in range(len(map_line)):
    garden.rst()
    if not garden.visited_pos[y][x]:
      garden.explore((y,x))
      total_fence += garden.compute_score()

print("Total fence:",  total_fence)







