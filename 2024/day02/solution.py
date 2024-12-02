import sys
import re
from functools import reduce
import math
import pyperclip

input = open(sys.argv[1]).read().strip()

p1 = 0
p2 = 0

# ---- CODE HERE ---- #


def sign(v) -> int:
    if v > 0:
        return 1
    if v < 0:
        return -1
    return 0

def is_unsafe(level) -> bool:
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

levels = []
for line in input.split("\n"):
    levels.append([int(n) for n in re.findall(r"(\d+)", line)])

count = 0
count2 = 0
for level in levels:
    if is_unsafe(level):
        count += 1

        could_be_safe = False
        for i in range(len(level)):
            new_level = level[:i] + level[i+1:]
            if not is_unsafe(new_level):
                could_be_safe = True
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
