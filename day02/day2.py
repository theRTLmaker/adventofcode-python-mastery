# -------- Day 2 --------
reports = []
with open("day2.txt", "r") as f:
    for line in f:
        reports.append(list(map(int, line.strip().split())))

# part 1
def safe_report(rep):
    # Check if the list has duplicates
    if len(rep) != len(set(rep)):
        return False

    # Check if list is in ascending order or descending order
    ascending = all(rep[i] < rep[i + 1] for i in range(len(rep) - 1))
    descending = all(rep[i] > rep[i + 1] for i in range(len(rep) - 1))

    # Check distance between adjacent numbers
    correct_distance = all(1 <= abs(rep[i] - rep[i + 1]) <= 3
                           for i in range(len(rep) - 1))

    if correct_distance and (ascending or descending):
        return True
    else:
        return False

safe_reports = 0
for num, rep in enumerate(reports):
    # Check if the list has duplicates
    if (safe_report(rep)):
        safe_reports += 1
print("Safe reports: ", safe_reports)

# part 2
safe_reports = 0
for num, rep in enumerate(reports):
    # Check if the list has duplicates
    if (safe_report(rep)):
        safe_reports += 1
    else:
        for remove in range(len(rep)):
            processed_rep = rep[:remove] + rep[remove+1:]
            if (safe_report(processed_rep)):
                safe_reports += 1
                break
print("Safe reports: ", safe_reports)
