import sys
import os

# Add the parent directory to sys.path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from progress_bar import progress_bar

# -------- Day 11 --------
# ----- part 1 -----
print("----- part 1 -----")

stones = []

with open("day11.txt", "r") as f:
	stones = list(map(int, f.readline().split(" ")))

# Rules:
# 0 -> 1
# len(str(stone)) % 2 == 0 -> split in half
# else -> multiply by 2024
print("stones:", stones)
total = 25
for blink in range(25):
	new_stones = []
	for stone in stones:
		if stone == 0:
			new_stones.append(1)
		elif len(str(stone)) % 2 == 0:
			str_stone = str(stone)
			len_stone = len(str_stone)
			first_half = int(str_stone[:len_stone//2])
			second_half = int(str_stone[len_stone//2:])
			new_stones.append(first_half)
			new_stones.append(second_half)
		else:
			new_stones.append(stone*2024)
	# print(blink+1, new_stones)
	stones = new_stones.copy()
	# Update the progress bar
	progress_bar(blink, total)


print()
# print(new_stones)
print("Hash:", len(stones))


# ----- part 2 -----
print("----- part 2 -----")

stones = []

with open("day11.txt", "r") as f:
	stones = tuple(map(int, f.readline().split(" ")))

# Rules:
# 0 -> 1
# len(str(stone)) % 2 == 0 -> split in half
# else -> multiply by 2024

def memoize(func):
    cache = {}
    def inner(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    return inner

from functools import cache
@cache
def transform(stone):
	if stone == 0:
		return (1,)

	str_stone = str(stone)
	len_stone = len(str_stone)
	if len_stone % 2 == 0:
		half_len = len_stone // 2
		return (int(str_stone[:half_len]), int(str_stone[half_len:]))

	return (stone*2024,)

print("stones:", stones)

@cache
def part2(input, iteration):
	# print("input", input)
	if iteration == 0:
		return len(input)

	return sum(part2(transform(n), iteration - 1) for n in input)




import time
print()
def run(stones, iter):
	start_time = time.time()
	print("Hash:", part2(stones, iter))
	end_time = time.time()

	execution_time = end_time - start_time
	print(f"Execution time for {iter}: {execution_time:.6f} seconds")


run(stones, 25)
run(stones, 30)
run(stones, 35)
run(stones, 40)
run(stones, 75)