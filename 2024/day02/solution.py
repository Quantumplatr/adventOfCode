import sys
import re
from functools import reduce
import math
import pyperclip

# Solved: 12/1/2024

# Things I could've done better:
# - Start with an is_safe function
# - I think is_safe might've been easier than is_unsafe. Eh.
# - Could've potentially compared diffs better/faster
#   Maybe `diffs = [level[i] - level[i+1] for i in range(len(level-1))]`
# - Could've potentially compared all increasing/decreasing faster
#   Use sorts? E.g. `if level != sorted_level or level != reverse_sorted_level`

input = open(sys.argv[1]).read().strip()

p1 = 0
p2 = 0

# ---- CODE HERE ---- #


def sign(v) -> int:
    """
    Return the sign of a value (1 if pos, -1 if neg, 0 if zero)
    """
    if v > 0:
        return 1
    if v < 0:
        return -1
    return 0

def is_unsafe(level) -> bool:
    """
    Reports if a level is unsafe.
    Unsafe if differences are not in range [1,3]
    Unsafe if not all increasing or not all decreasing
    """
    diff = 0
    prev = None
    prev_diff = None
    for n in level:
        if prev == None:
            prev = n
            continue
        
        diff = prev - n
        if prev_diff and sign(prev_diff) != sign(diff):
            return True
        prev_diff = diff

        if abs(diff) > 3 or diff == 0:
            return True

        prev = n

    return False

# Parse levels
levels = []
for line in input.split("\n"):
    levels.append([int(n) for n in re.findall(r"(\d+)", line)])

# Count unsafe levels
count = 0
count2 = 0
for level in levels:
    if is_unsafe(level):
        # If unsafe count for P1
        count += 1

        # Check all possibilities of removing 1 for P2
        could_be_safe = False
        for i in range(len(level)):
            # Remove index
            # E.g. i == 1: [1,2,3,4,5] -> [1,3,4,5]
            new_level = level[:i] + level[i+1:]
            # Check if safe
            if not is_unsafe(new_level):
                could_be_safe = True

        # Count for P2 if can't make safe with one change
        if not could_be_safe:
            count2 += 1

p1 = len(levels) - count
p2 = len(levels) - count2

# ------------------- #

print("Part 1:", p1)
print("Part 2:", p2)

to_copy = p1 if p2 == 0 else p2
pyperclip.copy(to_copy)
print(f"Copied {'P1' if p2 == 0 else 'P2'}: \"{to_copy}\"")
