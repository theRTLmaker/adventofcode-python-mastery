import sys
import os

# Add the parent directory to sys.path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from progress_bar import progress_bar

# -------- Day 25 --------
def parse_schematics(file_path):
    def parse_schematic(lines):
        """Converts a schematic to a tuple of column counts."""
        # Determine the column counts
        column_counts = [sum(1 for row in lines if row[col] == '#') - 1 for col in range(len(lines[0]))]
        return tuple(column_counts)

    locks = []
    keys = []
    with open(file_path, 'r') as file:
        # Read the file content
        content = file.read().strip()
        # Split by double newline to separate schematics
        schematic_blocks = content.split('\n\n')

        for block in schematic_blocks:
            # Split into lines and strip whitespace
            lines = [line.strip() for line in block.split('\n') if line.strip()]

            if len(lines) == 7 and lines[0].startswith('#'):
                # Lock schematic: top row is full of '#'
                locks.append(parse_schematic(lines))
            elif len(lines) == 7 and lines[-1].startswith('#'):
                # Key schematic: bottom row is full of '#'
                keys.append(parse_schematic(lines))

    return locks, keys

# Example usage
file_path = 'day25.txt'
locks, keys = parse_schematics(file_path)

# print("Locks:")
# for lock in locks:
#     print(lock)
# print("Keys:")
# for key in keys:
#     print(key)


# ----- part 1 -----
print("-------------")
print("Part 1")

def count_key_lock_matches(keys, locks):
    """Counts the total number of matches where a key can open a lock."""
    count = 0
    for key in keys:
        for lock in locks:
            if all(k + l <= 5 for k, l in zip(key, lock)):
                count += 1
    return count

count = count_key_lock_matches(keys, locks)

print(f"The total number is {count}")

# ----- part 2 -----
print("-------------")
print("Part 2")

# print(f"The maximum lan party is {max_clique}")
