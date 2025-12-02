import sys
import os

# Add the parent directory to sys.path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from progress_bar import progress_bar

[]

# -------- Day 9 --------
# ----- part 1 -----
print("----- part 1 -----")

raw_disk = []

with open("day09.txt", "r") as f:
  raw_disk = list(f.readline())

disk = []
enable = True

for id, entry in enumerate(raw_disk):
    if enable:
        disk += ([str(id//2)] * int(entry))
        enable = False
    else:
        disk += (["."] * int(entry))
        enable = True

dest_pos = 0
source_pos = len(disk) - 1

while dest_pos < source_pos:
    # Iterate dest_post until finding "."
    while disk[dest_pos] != "." and dest_pos < source_pos:
        dest_pos += 1
    # Iterate source_pos until finding non "."
    while disk[source_pos] == "." and dest_pos < source_pos:
        source_pos -= 1

    disk[dest_pos] = disk[source_pos]
    disk[source_pos] = "."

checksum = 0
for i, entry in enumerate(disk):
    if entry == ".":
        break
    checksum += i * int(entry)

print("checksum", checksum)

# ----- part 2 -----
print("----- part 2 -----")

disk_data = []
enable = True

for id, entry in enumerate(raw_disk):
    if enable:
        disk_data.append([int(entry), int(id//2)])
        enable = False
    else:
        disk_data.append([int(entry), -1])
        enable = True


print("disk_data", raw_disk)
print("disk_data", disk_data)

i = len(disk_data) - 1
if disk_data[-1][1] != -1:
    current_id = disk_data[-1][1] + 1
else:
    current_id = disk_data[-2][1] + 1

def print_disk_data(disk_data):
    for len, id in disk_data:
        if id != -1:
            print(f"{id}" * int(len), end="")
        else:
            print("." * int(len), end="")
    print()

def create_disk_data(disk_data):
    disk = []
    for len, id in disk_data:
        if id != -1:
            disk += [id] * len
        else:
            disk += ["."] * len
    print(disk)
    return disk

total = len(disk_data)

while i > 0:

    if disk_data[i][1] == -1:
        i -= 1
        continue

    if disk_data[i][1] >= current_id:
        i -= 1
        continue

    moved = False

    def find_index(disk, entry, max_i):
        return next((i for i, (len, id) in enumerate(disk) if id == -1 and len >= entry and i < max_i), -1)

    index = find_index(disk_data, disk_data[i][0], i)

    if index != -1:
        len = disk_data[i][0]
        id = disk_data[i][1]
        disk_data[i][1] = -1
        disk_data.insert(index, [len, id])

        if disk_data[index+1][0] > len:
            disk_data[index+1][0] -= len
        else:
            del disk_data[index + 1]
        moved = True
        current_id = id

    # print_disk_data(disk_data)

    # Update the progress bar
    progress_bar(i, total)
    if not moved:
        i -= 1

print()

checksum = 0
for i, entry in enumerate(create_disk_data(disk_data)):
    if entry != ".":
        checksum += i * entry

print("checksum", checksum)

# we are missing the thing that breaks searching when we already searched all the elements