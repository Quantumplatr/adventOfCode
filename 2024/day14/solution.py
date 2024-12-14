import enum
import sys
import re
from functools import reduce
import math
import pyperclip

# Solved: 2024-12-13
# Things to improve:
# - Did *okay* on P1. Could've done better printing the output.
#   Fastest part was `place` function. Messed up my quadrant checks.
#   Pretty tired today
# - Got a hint for P2. I was just looking manually. Saw a hint that
#   it would be no overlap. Tried that and found one before no the tree
#   with no overlap but then just got the second w/ no overlap.
#   I was worried it would be some pattern to look for but I wouldn't know what pattern
#   but also that it might not be a straightforward pattern (I was right as it
#   was not centered).
# - Anyway. Fairly happy. Just not super speedy. And I did get a touch of help.

input = open(sys.argv[1]).read().strip()

p1 = 0
p2 = 0

# ---- CODE HERE ---- #

robots = []
for line in input.split("\n"):
    pv = re.findall(r"((-*\d+),(-*\d+))", line)
    p = [int(n) for n in pv[0][1:]]
    v = [int(n) for n in pv[1][1:]]
    robots.append({"p": p, "v": v})

# width = 11
# height = 7

width = 101
height = 103


# Get resulting location of robot after
# duration
def place(robot, dur):
    p = robot["p"]
    v = robot["v"]

    px, py = p
    vx, vy = v

    x = px + vx * dur
    y = py + vy * dur

    return (x % width, y % height)


# Pretty print position
# If `hide_middle`, use "x" for center row and col
def print_robots(positions, hide_middle=False):
    grid = []
    for i in range(height):
        grid.append([0] * width)

    for p in positions:
        x, y = p
        grid[y][x] += 1

    for i, r in enumerate(grid):
        to_print = list(r)

        if hide_middle:
            if i == int(height / 2):
                to_print = ["x" for n in to_print]

            to_print[int(width / 2)] = "x"

        print("".join([str(n) if n != 0 else "." for n in to_print]))


q1 = 0
q2 = 0
q3 = 0
q4 = 0
positions = []
for robot in robots:
    # Get robot position
    x, y = place(robot, 100)
    positions.append((x, y))

    # Get quadrant
    # NOTE: probably a much better way
    if x != int(width / 2) and y != int(height / 2):
        if x < int(width / 2):
            if y < int(height / 2):
                q1 += 1
            else:
                q2 += 1
        elif x > int(width / 2):
            if y > int(height / 2):
                q3 += 1
            else:
                q4 += 1

# P1 solution
p1 = q1 * q2 * q3 * q4

# Loop until positions have no overlap
positions = []
for robot in robots:
    x, y = place(robot, 0)
    positions.append((x, y))
i = 0
# Specifically, find two w/ no overlap
# b/c first wasn't the right answer
found_count = 0
while found_count < 2:
    i += 1
    positions = []
    for robot in robots:
        x, y = place(robot, i)
        positions.append((x, y))

    if len(set(positions)) == len(positions):
        found_count += 1

# Print to confirm that it's a tree
print_robots(positions)
print(i)  # Print P2

# ------------------- #

print("Part 1:", p1)
print("Part 2:", p2)

to_copy = p1 if p2 == 0 else p2
pyperclip.copy(to_copy)
print(f"Copied {'P1' if p2 == 0 else 'P2'}: \"{to_copy}\"")
