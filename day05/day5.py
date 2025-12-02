# -------- Day5 --------
# part 1
# Example usage
pairs = [(47, 53), (97, 13), (97, 61), (97, 47), (75, 29), (61, 13), (75, 53),
         (29, 13), (97, 29), (53, 29), (61, 53), (97, 53), (61, 29), (47, 13),
         (75, 47), (97, 75), (47, 61), (75, 61), (47, 29), (75, 13), (53, 13)]

rules = {}
i = 0
with open("day5.txt", "r") as f:
  for line in f:
    parent, child = line.split('|')
    parent = int(parent)
    child = int(child)

    if not (parent in rules):
      rules[parent] = [child]
    else:
      rules[parent].append(child)

# print(rules)
sequences = []
with open("day5-2.txt", "r") as f:
  for line in f:
    sequences.append([int(num) for num in list(line.split(','))])

correct_sequences = []
incorrect_sequences = []
nb_false = 0

for seq in sequences:
  correct = True
  for i, num in enumerate(seq[::-1]):
    ii = len(seq) - i
    if not correct:
      break

    # print('rules', num, sorted(rules[num]))
    # print(ii, 'seq short', seq[:ii-1])

    if any(item in rules[num] for item in seq[:ii - 1]):
      correct = False
      nb_false = nb_false + 1
      # print("False", ii)
      incorrect_sequences.append(seq)

  if correct:
    # print("Correct")
    correct_sequences.append(seq)

sum = 0

for seq in correct_sequences:
  middle_index = len(seq) // 2

  # Get the value at the middle index
  middle_value = seq[middle_index]

  sum += middle_value

print(sum)
print("nb false=", nb_false)

# part 2
# While the Elves get to work printing the correctly-ordered updates, you have a little time to fix the rest of them.

# For each of the incorrectly-ordered updates, use the page ordering rules to put the page numbers in the right order. For the above example, here are the three incorrectly-ordered updates and their correct orderings:

# 75,97,47,61,53 becomes 97,75,47,61,53.
# 61,13,29 becomes 61,29,13.
# 97,13,75,29,47 becomes 97,75,47,29,13.
# After taking only the incorrectly-ordered updates and ordering them correctly, their middle page numbers are 47, 29, and 47. Adding these together produces 123.

# Find the updates which are not in the correct order. What do you get if you add up the middle page numbers after correctly ordering just those updates?

print("--------")
print("# part 2")
print("--------")
corrected_sequences = []
for seq_nb, seq in enumerate(incorrect_sequences):
  print(seq, len(seq))
  correct = False
  print("Progress", seq_nb, "/", len(incorrect_sequences))

  run_seq = seq.copy()
  cor_seq = seq.copy()
  while (not correct):
    run_seq = cor_seq.copy()
    for i, num in enumerate(run_seq[::-1]):
      ii = len(seq) - i
      if ii == 1:
        correct = True
        print('CORRECT')
        break

      # print('rules', num, sorted(rules[num]))
      # print(ii, 'seq short', seq[:ii-1])

      apply_rule = [item in rules[num] for item in run_seq[:ii - 1]]
      if any(apply_rule):
        # print("False", ii-1, apply_rule)
        last_true_index = len(apply_rule) - 1 - apply_rule[::-1].index(True)
        # print(last_true_index)

        # Fix it
        cor_seq = run_seq.copy()
        cor_seq[ii - 1] = cor_seq[last_true_index]
        cor_seq[last_true_index] = num
        # print(cor_seq)
        break  # go to while

  corrected_sequences.append(cor_seq)

  print(cor_seq, "-", cor_seq[len(cor_seq)//2])

# Verifying corrected_sequences with 1st part
correct_sequences = []
for seq in corrected_sequences:
  correct = True
  for i, num in enumerate(seq[::-1]):
    ii = len(seq) - i
    if not correct:
      break

    # print('rules', num, sorted(rules[num]))
    # print(ii, 'seq short', seq[:ii-1])

    if any(item in rules[num] for item in seq[:ii - 1]):
      correct = False
      nb_false = nb_false + 1
      print("ERROR !!!!", ii)

      incorrect_sequences.append(seq)

  if correct:
    # print("Correct")
    correct_sequences.append(seq)

sum = 0

for seq in correct_sequences:
  middle_index = len(seq) // 2

  # Get the value at the middle index
  middle_value = seq[middle_index]
  sum += middle_value

print("Finished", sum)
print("num corrected ", len(correct_sequences))
