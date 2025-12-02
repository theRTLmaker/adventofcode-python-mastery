map=[]
with open('map.txt', 'r') as file:
  # Read all lines from the file
  for lines in file:
    map_tmp = list(lines.strip())
    map.append([int(x) for x in map_tmp])



# Strip any leading/trailing whitespace characters from each line

# print(map)

# Class trailhead
# score
# current position
# nine_position
# def explore():
# iterate through each direction
# if next_pos == 9
#   add unique pos to nine_position
#   ret
# if next_pos == pos + 1:
#   pos = next_pos;
#   explore()

class Trailhead:
  def __init__(self,initial_pos):
    self.score = 0
    self.initial_pos = initial_pos
    self.nine_positions = set()    # Set to store unique positions where value 9 is found


  def explore(self, grid, position=None):
    """
    Recursive function to explore the grid in all directions.
    :param grid: 2D list representing the grid
    :param position: Current position (row, col) as a tuple
    """

    if position is None:
        position = self.initial_pos

    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up
    for direction in directions:
        next_pos = (position[0] + direction[0], position[1] + direction[1])

        # Ensure the next position is within bounds
        if 0 <= next_pos[0] < len(grid) and 0 <= next_pos[1] < len(grid[0]):
            value = grid[next_pos[0]][next_pos[1]]
            # print(value)
            if value == grid[position[0]][position[1]] + 1:
                if value == 9:
                    self.nine_positions.add(next_pos)
                    self.score += 1
                    # return  # Stop further exploration in this direction
                else:

                    self.explore(grid, next_pos)     # Recursive call




  def compute_score(self):
    # print(self.nine_positions)
    # self.score = len(self.nine_positions)
    return self.score

total_score = 0
for y, map_line in enumerate(map):
  for x in range(len(map_line)):
    if map[y][x] == 0:
      trail = Trailhead((y,x))
      trail.explore(map)
      total_score += trail.compute_score()
      # print("score", trail.score, "init pos", (y,x))
print("total_score=",  total_score)