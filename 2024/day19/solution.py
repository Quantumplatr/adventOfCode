import sys
import re
from functools import reduce
import math
import pyperclip

# Solved: 2024-12-18
# Rank: 823/1713
# Time: 00:07:25/00:21:08
#
# Pretty happy with today's solution. Had the concept down for both quite quick.
# Just some simple backtracking. No real issues w/ P1. Could've done it faster
# I guess. P2 I got caught up on 2 things. I was recursing with the wrong function
# for a while. If I had caught that sooner, I would've solved this much, much
# faster I think. The other issue I had was I had `count` in my cache key which
# didn't break anything but made my cache hit's less frequent so it ran much slower.
#
# Next time: be more careful copy pasting P1 func to P2 func

input = open(sys.argv[1]).read().strip()

p1 = 0
p2 = 0

# ---- CODE HERE ---- #

# Parse input
towels, patterns = input.split("\n\n")
towels = towels.split(", ")
patterns = patterns.split("\n")


# Backtrack the ways that `towels` can build `pattern`
# `t_so_far` is an array of values of `towels`.
# Returns None if no way to make `pattern`.
# Returns how many towels it takes to make `pattern`.
#
# I'm realizing now that this doesn't really matter.
# It's more of a True/False needed for P1. Anyways, it works.
# It also doesn't return a min count lmao. Oh well.
def backtrack(pattern: str, towels, t_so_far, count):
    # Invalid
    if not pattern.startswith("".join(t_so_far)):
        return None

    # End case
    if pattern == "".join(t_so_far):
        return count

    # Try all next towels
    for t in towels:
        c = backtrack(pattern, towels, t_so_far + [t], count + 1)
        if c is not None:
            return c

    # Found no options
    return None


# Cache
seen = {}


# Backtrack the ways that `towels` can build `pattern`
# `t_so_far` is an array of values of `towels`.
# Returns `None` if no ways to build `pattern`.
# Returns the number of ways `towels` can build `pattern`.
def backtrack2(pattern: str, towels, t_so_far):
    # Cache key
    key = (pattern, "".join(t_so_far))
    # Cache check
    if key in seen:
        return seen[key]

    # Invalid
    if not pattern.startswith("".join(t_so_far)):
        seen[key] = None
        return None

    # End case
    if pattern == "".join(t_so_far):
        seen[key] = 1
        return 1

    # Try all next towels
    cs = 0
    for t in towels:
        c = backtrack2(pattern, towels, t_so_far + [t])
        # If found some solutions, add count
        if c is not None:
            cs += c

    seen[key] = cs
    return cs


# P1
for pattern in patterns:
    count = backtrack(pattern, towels, [], 0)
    if count is not None:
        p1 += 1

# P2
for pattern in patterns:
    count = backtrack2(pattern, towels, [])
    if count is not None:
        p2 += count

# ------------------- #

print("Part 1:", p1)
print("Part 2:", p2)

to_copy = p1 if p2 == 0 else p2
pyperclip.copy(to_copy)
print(f"Copied {'P1' if p2 == 0 else 'P2'}: \"{to_copy}\"")
