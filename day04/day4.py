# -------- Day 4 --------
# part 1
class StateManager:
  VALID_STATES = {'X', 'M', 'A', 'S'}

  def __init__(self, initial_state: str = 'X'):
    """
      Initialize the StateManager with a given state.
      :param initial_state: The initial state, must be one of 'X', 'M', 'A', 'S'.
      """
    if initial_state not in self.VALID_STATES:
      raise ValueError(
          f"Invalid state '{initial_state}'. Must be one of {self.VALID_STATES}."
      )
    self._state = initial_state

  @property
  def state(self) -> str:
    """Get the current state."""
    return self._state

  @state.setter
  def state(self, new_state: str):
    """Set the state to a new value, ensuring it's valid."""
    if new_state not in self.VALID_STATES:
      raise ValueError(
          f"Invalid state '{new_state}'. Must be one of {self.VALID_STATES}.")
    self._state = new_state

  def toggle(self):
    """
      Cycle through states in order: X -> M -> A -> S -> X.
      """
    state_order = ['X', 'M', 'A', 'S']
    current_index = state_order.index(self._state)
    self._state = state_order[(current_index + 1) % len(state_order)]

  def reset(self):
    """
    Sets the states back to X.
    """
    self.state = 'X'

  def __str__(self):
    """Return a string representation of the current state."""
    return f"Current state: {self._state}"


#               up,    right,   down,   left,   up/right, down/left  down/right  up/left
search_dir = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1),
              (-1, 1)]
state = StateManager()
word_matrix = []
with open("day4.txt", "r") as f:
  for line in f:
    word_matrix.append(list(line.strip()))


# assuming the word matrix is a matrix
def is_position_in_matrix(x: int, y: int, matrix: list) -> bool:
  """
  Check if a given (x, y) position is within the bounds of a 2D matrix.

  :param x: The row index.
  :param y: The column index.
  :param matrix: The 2D matrix (a list of lists).
  :return: True if the position is within bounds, False otherwise.
  """
  if not matrix:
    return False  # Return False for an empty matrix

  num_rows = len(matrix)
  num_cols = len(matrix[0]) if num_rows > 0 else 0

  return 0 <= x < num_rows and 0 <= y < num_cols


xmas_count = 0


def check_adjacent_letter(x: int, y: int, direction: tuple,
                          state: StateManager):
  global xmas_count
  global word_matrix
  x = x + direction[0]
  y = y + direction[1]
  if is_position_in_matrix(x, y, word_matrix):
    if word_matrix[x][y] == state.state:
      if (state.state == 'S'):
        xmas_count += 1
        return
      state.toggle()
      check_adjacent_letter(x, y, direction, state)

  return


for i in range(len(word_matrix)):
  for j in range(len(word_matrix[i])):
    state.reset()
    letter = word_matrix[i][j]
    if letter == 'X':
      state.toggle()
      for direction in search_dir:
        state.reset()
        state.toggle()
        check_adjacent_letter(i, j, direction, state)

print(xmas_count)

# part 2
x_counter = 0

filters = [[['M', '', 'M'], ['', 'A', ''], ['S', '', 'S']],
           [['M', '', 'S'], ['', 'A', ''], ['M', '', 'S']],
           [['S', '', 'S'], ['', 'A', ''], ['M', '', 'M']],
           [['S', '', 'M'], ['', 'A', ''], ['S', '', 'M']]]

correct = True
for i in range(len(word_matrix) - 2):
  for j in range(len(word_matrix[i]) - 2):
    for filter in filters:
      correct = True
      for x in range(len(filter)):
        for y in range(len(filter[x])):
          if filter[x][y] != "" and word_matrix[i + x][j + y] != filter[x][y]:
            correct = False
            break
        if not correct:
          break
      if correct:
        x_counter += 1

print(x_counter)
