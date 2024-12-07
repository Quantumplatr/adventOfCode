import sys
import re
from functools import reduce
import math
import pyperclip

# Solved: 12/6/2024
# Things I could do better:
# - I think I knew the solution super quick
#   I'm just really rusty on my recursion/backtracking
# - Could've backtracked better. Just short circuits I think:
#   - Return if total is unattainable (e.g. value > goal)

input = open(sys.argv[1]).read().strip()

p1 = 0
p2 = 0

# ---- CODE HERE ---- #


# Recursively try all options
def calc(value, usable):
    if len(usable) == 0:
        return [value]

    adds = calc(value + usable[0], usable[1:])
    mults = calc(value * usable[0], usable[1:])
    concats = calc(int(str(value) + str(usable[0])), usable[1:])

    return adds + mults + concats


# If there is any combo that results in the total, return True
def can_equal(total, usable) -> bool:
    options = calc(0, usable)

    return total in options


# Split into lines
for line in input.split("\n"):
    # E.g. 190: 10 19
    nums = re.findall(r"(\d+)", line)

    # First number is total (E.g. 190)
    total = int(nums[0])
    # Rest of the numbers are usable for calculation (e.g. [10,19])
    usable = [int(n) for n in nums[1:]]

    # Sum totals attainable
    # P1 doesn't use `concats` in `calc`
    if can_equal(total, usable):
        p1 += total


# ------------------- #

print("Part 1:", p1)
print("Part 2:", p2)

to_copy = p1 if p2 == 0 else p2
pyperclip.copy(to_copy)
print(f"Copied {'P1' if p2 == 0 else 'P2'}: \"{to_copy}\"")
