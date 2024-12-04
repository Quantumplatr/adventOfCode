import sys
import re
from functools import reduce
import math
import pyperclip

# Solved: 12/2/2024
#
#        | Time     | Rank
# -------+----------+-----
# Part 1 | 00:02:16 |  289
# Part 2 | 00:12:59 | 1792
#
# Things to improve:
# - I'm actually pretty proud of my part 1.
#   Idk what I would've improved. Maybe the regex so I don't findall twice
#   and go straight to an array of pairs. I assume that's possible.
# - Part 2 I started with trying to use regex. That was a mistake b/c I'm
#   not THAT familiar with regex for lookaheads/behinds.
# - Could've been a little faster/cleaner with my part 2 just in execution
#   but I'm pretty happy w/ my perfomance

input = open(sys.argv[1]).read().strip()

p1 = 0
p2 = 0

# ---- CODE HERE ---- #

# Get all instances of "mul(<number>,<number>)"
muls = re.findall(r"(mul\(\d+,\d+\))", input)

# - Shorter Code - #
pairs = re.findall(r"(mul\((\d+),(\d+)\))", input)
p1 = sum([int(pair[1]) * int(pair[2]) for pair in pairs])

# - Original Code - #
# Calculate sum of a*b for each a,b pair
# for mul in muls:
#     a, b = re.findall(r"(\d+)", mul)
#     p1 += int(a) * int(b)

# Do the same as above but only if there was a `do()` or `start of line`
# more recent than a `don't()`
i = 0
can_mult = True
# Iterate through input
while i < len(input):

    # Get substring
    curr = input[i:]
    
    # Check if we're at a do or don't
    if curr.startswith("don't()"):
        can_mult = False
    if curr.startswith("do()"):
        can_mult = True

    # If can mult, check for a mult.
    if can_mult:
        # Initially did a findall. After solving, I changed it to match.
        match = re.match(r"^mul\((\d+),(\d+)\)", curr)
        if match:
            a,b = match.group(1,2)
            p2 += int(a) * int(b)

    i += 1

# ------------------- #

print("Part 1:", p1)
print("Part 2:", p2)

to_copy = p1 if p2 == 0 else p2
pyperclip.copy(to_copy)
print(f"Copied {'P1' if p2 == 0 else 'P2'}: \"{to_copy}\"")
