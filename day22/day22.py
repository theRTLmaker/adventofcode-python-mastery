import sys
import os

# Add the parent directory to sys.path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from progress_bar import progress_bar

# -------- Day 22 --------
def load_init_numbers(file_path):
	with open(file_path, 'r') as file:
		lines = file.readlines()

	# Remove any trailing whitespace or newlines
	init_numbers = [int(line.strip()) for line in lines]

	return init_numbers

file_path = "day22.txt"
init_numbers = load_init_numbers(file_path)

# ----- part 1 -----
print("-------------")
print("Part 1")

from functools import cache

@cache
def mix(secret, value):
	return secret ^ value

@cache
def prune(secret):
	return secret % 16777216

@cache
def calculate_next(secret):
	secret = prune(mix(secret, secret * 64))
	secret = prune(mix(secret, secret // 32))
	secret = prune(mix(secret, secret * 2048))

	return secret

nb_ite = 2000
running_total = 0
for i, nb in enumerate(init_numbers):
	progress_bar(i, len(init_numbers))
	secret = nb
	for ite in range(nb_ite):
		secret = calculate_next(secret)
	# print(f"{nb}: {secret}")
	running_total += secret

print()
print()
print(f"Total: {running_total}")

# ----- part 2 -----
print("-------------")
print("Part 2")

nb_ite = 2000

def generate_all_bananas(init_numbers):
	seqs = []
	for i, nb in enumerate(init_numbers):
		progress_bar(i, len(init_numbers))
		seq = []
		secret = nb
		for _ in range(nb_ite):
			new_secret = calculate_next(secret)
			seq.append(new_secret%10)
			secret = new_secret
		seqs.append(tuple(seq))

	print()

	return seqs

print("Generating all banana prices")
bananas_seq = generate_all_bananas(init_numbers)

def generate_all_diffs(seqs):
	diffs = []
	for seq in seqs:
		diff = []
		for i in range(len(seq)-1):
			diff.append(seq[i+1] - seq[i])
		diffs.append(diff)
	return diffs


print("Generating all price difference")
diffs_seq = generate_all_diffs(bananas_seq)


print("Computing best sequence")
best_seqs = {}
for i, seq in enumerate(diffs_seq):
	combs = set()

	progress_bar(i, len(diffs_seq))
	# print("--------")
	for s1, s2, s3, s4, banana in zip(seq, seq[1:], seq[2:], seq[3:], bananas_seq[i][4:]):
		# Only check the first time a combo shows up
		if (s1, s2, s3, s4) in combs:
			continue

		# Add tried combo
		combs.add((s1, s2, s3, s4))
		if (s1, s2, s3, s4) in best_seqs:
			best_seqs[(s1, s2, s3, s4)] += banana
		else:
			best_seqs[(s1, s2, s3, s4)] = banana
		# print((s1, s2, s3, s4), banana, best_seqs[(s1, s2, s3, s4)])

print()
print()
print(f"Best: {max(best_seqs, key=best_seqs.get)} with {max(best_seqs.values())} bananas")