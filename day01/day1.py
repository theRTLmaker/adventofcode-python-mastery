# -------- Day 1 --------
first_ints = []
second_ints = []
with open("day1.txt", "r") as f:
    for line in f:
        num1, num2 = map(int, line.split())
        first_ints.append(num1)
        second_ints.append(num2)

if len(first_ints) != len(second_ints):
    print("The lists are not the same size")

first_ints.sort()
second_ints.sort()

# part 1
total_dist = 0
for i in range(len(first_ints)):
    dist = abs(first_ints[i] - second_ints[i])
    total_dist += dist
print("distance: ", total_dist)

# part 2
total_sim = 0
for i in range(len(first_ints)):
    count = second_ints.count(first_ints[i])
    total_sim += first_ints[i] * count
print("similarity: ", total_sim)