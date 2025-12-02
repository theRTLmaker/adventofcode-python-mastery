import sys
import os

# Add the parent directory to sys.path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from progress_bar import progress_bar

# -------- Day 8 --------
# ----- part 1 -----
print("----- part 1 -----")

antenas = {}
sizeX = 0
sizeY = 0

with open("day08.txt", "r") as f:
  for x, line in enumerate(f):
    sizeX += 1
    sizeY = len(list(line))
    for y, entry in enumerate(list(line)):
      if entry != "." and entry != "\n":
        if entry in antenas:
          antenas[entry].append((x, y))
        else:
          antenas[entry] = [(x, y)]

def plot_matrix(coord1, coord2, anti1, anti2):
    """
    Plots a matrix with given coordinates and anti-coordinates.

    Args:
        coord1 (tuple): First coordinate (x, y) for 'O'.
        coord2 (tuple): Second coordinate (x, y) for 'O'.
        anti1 (tuple or bool): First anti-coordinate (x, y) for 'X' or False to ignore.
        anti2 (tuple or bool): Second anti-coordinate (x, y) for 'X' or False to ignore.
    """

    # Create the matrix
    matrix = [['.' for _ in range(sizeY)] for _ in range(sizeX)]

    # Place coordinates
    if 0 <= coord1[0] < sizeX and 0 <= coord1[1] < sizeY:
        matrix[coord1[0]][coord1[1]] = 'O'
    if 0 <= coord2[0] < sizeX and 0 <= coord2[1] < sizeY:
        matrix[coord2[0]][coord2[1]] = 'O'

    # Place anti-coordinates if provided
    if not isinstance(anti1, list):
      if anti1 and 0 <= anti1[0] < sizeX and 0 <= anti1[1] < sizeY:
          matrix[anti1[0]][anti1[1]] = 'X'
    else:
      for anti in anti1:
        if anti and 0 <= anti[0] < sizeX and 0 <= anti[1] < sizeY:
          matrix[anti[0]][anti[1]] = 'X'
    if not isinstance(anti2, list):
      if anti2 and 0 <= anti2[0] < sizeX and 0 <= anti2[1] < sizeY:
          matrix[anti2[0]][anti2[1]] = 'X'
    else:
      for anti in anti2:
        if anti and 0 <= anti[0] < sizeX and 0 <= anti[1] < sizeY:
          matrix[anti[0]][anti[1]] = 'X'

    # Print the matrix
    for row in matrix:
        print(' '.join(row))

cum_matrix = [['.' for _ in range(sizeY)] for _ in range(sizeX)]
def cumulative_matrix(coord1, coord2, anti1, anti2):
  global cum_matrix

  # Place coordinates
  if 0 <= coord1[0] < sizeX and 0 <= coord1[1] < sizeY:
      cum_matrix[coord1[0]][coord1[1]] = 'O'
  if 0 <= coord2[0] < sizeX and 0 <= coord2[1] < sizeY:
      cum_matrix[coord2[0]][coord2[1]] = 'O'

  # Place anti-coordinates if provided
  if not isinstance(anti1, list):
    if anti1 and 0 <= anti1[0] < sizeX and 0 <= anti1[1] < sizeY:
        cum_matrix[anti1[0]][anti1[1]] = 'X'
  else:
    for anti in anti1:
      if anti and 0 <= anti[0] < sizeX and 0 <= anti[1] < sizeY:
        cum_matrix[anti[0]][anti[1]] = 'X'
  if not isinstance(anti2, list):
    if anti2 and 0 <= anti2[0] < sizeX and 0 <= anti2[1] < sizeY:
        cum_matrix[anti2[0]][anti2[1]] = 'X'
  else:
    for anti in anti2:
      if anti and 0 <= anti[0] < sizeX and 0 <= anti[1] < sizeY:
        cum_matrix[anti[0]][anti[1]] = 'X'

def plot_cum_matrix(cum_matrix):
  sum = 0
  # Print the matrix
  for row in cum_matrix:
    sum+=len(row) - row.count(".")
    print(' '.join(row), len(row) - row.count("."))
  print(sum)

def is_inside_matrix(coord):
    """
    Check if a given coordinate is inside the matrix bounds.

    Args:
        coord (tuple): A tuple (x, y) representing the coordinate.

    Returns:
        bool: True if the coordinate is inside the matrix, False otherwise.
    """
    x, y = coord
    if 0 <= x < sizeX and 0 <= y < sizeY:
      return (x, y)

    return False


def compute_antinodes(x1, y1, x2, y2):
  distX = x2 - x1
  distY = y2 - y1

  # Compute antinode 1
  anti1 = is_inside_matrix((x1 - distX, y1 - distY))
  # Compute antinode 2
  anti2 = is_inside_matrix((x2 + distX, y2 + distY))
  return anti1, anti2

antinode = set()

total = len(antenas.keys())
from itertools import combinations
for i, coords in enumerate(antenas.values(), start=1):
  for coord1, coord2 in combinations(coords, 2):
    anti1, anti2 = compute_antinodes(coord1[0], coord1[1], coord2[0], coord2[1])
    if anti1:
      antinode.add((anti1))
    if anti2:
      antinode.add((anti2))

  # Update the progress bar
  progress_bar(i, total)

print("Number of unique antinodes:", len(antinode))

# ----- part 2 -----
print("----- part 2 -----")

def compute_harm_antinodes(x1, y1, x2, y2):
  distX = x2 - x1
  distY = y2 - y1

  # Compute antinode 1
  anti1 = []
  anti = (x1, y1)
  while True:
    anti = is_inside_matrix((anti[0] - distX, anti[1] - distY))
    if anti == False:
      break
    anti1.append(anti)

  # Compute antinode 2
  anti2 = []
  anti = (x2, y2)
  while True:
    anti = is_inside_matrix((anti[0] + distX, anti[1] + distY))
    if anti == False:
      break
    anti2.append(anti)

  return anti1, anti2

antinode = set()

total = len(antenas.keys())
from itertools import combinations
for i, coords in enumerate(antenas.values(), start=1):
  for coord1, coord2 in combinations(coords, 2):
    anti1, anti2 = compute_harm_antinodes(coord1[0], coord1[1], coord2[0], coord2[1])
    # print(coord1, coord2)
    # print(anti1, anti2)
    antinode.add((coord1))
    antinode.add((coord2))
    for anti in anti1:
      antinode.add((anti))
    for anti in anti2:
      antinode.add((anti))
    # cumulative_matrix(coord1, coord2, anti1, anti2)
    # print()
    # print()
    # print()

  # Update the progress bar
  progress_bar(i, total)

# plot_cum_matrix(cum_matrix)
print("Number of unique harmonique antinodes:", len(antinode))
