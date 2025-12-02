# -------- Day 7 --------
# part 1
print("Part 1")
data = []

with open("day7.txt", "r") as f:
  for line in f:
    parts = line.split(':')
    assert (len(parts) == 2)
    result = int(parts[0].strip())
    numbers = list(map(int, parts[1].strip().split(' ')))

    data.append((result, numbers))

import math
from itertools import product


def apply_op(numbers, operators):
  assert (len(operators) == len(numbers) - 1)
  result = numbers[0]
  for i in range(len(operators)):
    if operators[i] == '+':
      result += numbers[i + 1]
    elif operators[i] == '*':
      result *= numbers[i + 1]
  return result


def generate_combinations_iterable(l):
  """
  Generate all possible combinations of '+' and '*' of length l as an iterable.

  Args:
      l (int): The length of each combination.

  Yields:
      list: Each combination of '+' and '*', one at a time.
  """
  # Use itertools.product to lazily generate combinations
  for comb in product('+*', repeat=l):
    yield list(comb)  # Convert the tuple to a list and yield it


sum_valid_results = 0
incorrect_data = []
for result, numbers in data:
  correct = False
  for operators in generate_combinations_iterable(len(numbers) - 1):
    if result == apply_op(numbers, operators):
      sum_valid_results += result
      correct = True
      break

  if correct == False:
    incorrect_data.append((result, numbers))

print('sum_valid_results', sum_valid_results)

# part 2
print('Part 2')


# import functools
# @functools.lru_cache
def generate_combinations_iterable2(l):
  """
  Generate all possible combinations of '+' and '*' of length l as an iterable.

  Args:
      l (int): The length of each combination.

  Yields:
      list: Each combination of '+' and '*', one at a time.
  """
  # Use itertools.product to lazily generate combinations
  for comb in product('+|*', repeat=l):
    yield list(comb)  # Convert the tuple to a list and yield it


def apply_op2(numbers, operators):
  assert (len(operators) == len(numbers) - 1)

  # Logic to process concatenation
  result = numbers[0]  # Start with the first number as a string

  for i in range(len(operators)):
    if operators[i] == '|':  # Handle concatenation at this index
      result = int(str(result) + str(numbers[i + 1]))  # Concatenate the number
    elif operators[i] == '+':
      result += numbers[i + 1]
    elif operators[i] == '*':
      result *= numbers[i + 1]

  return result


from progress_bar import progress_bar

total = len(incorrect_data)
for i, (result, numbers) in enumerate(incorrect_data, start=1):
  for operators in generate_combinations_iterable2(len(numbers) - 1):
    if result == apply_op2(numbers, operators):
      sum_valid_results += result
      # print('Correct', (result, numbers))
      break
  # Update the progress bar
  progress_bar(i, total)

print('sum_valid_results', sum_valid_results)
