import sys
import re
from functools import reduce
import math
import pyperclip

# Solved: 2024-12-11
#
# P1 Things to Improve:
# - My BFS was a bit slow for me to implement.
# - I also forgot to check that the neighbors were the same char.
# - My first permimeter idea was wrong and it took me a bit to
#   figure out to track borders (or where the BFS failed).
# - Just a bit of a slow start.
#
# P2 Things to Improve:
# - P2 stumped me for a while
# - I had a rough idea how to solve it pretty quick
#   but I ran into lots of issues along the way. I knew that I should
#   search the borders to find the subsets that were in a line.
# - I started off rough and started the function from scratch again
# - I started with trying to look at all other border coords from each
#   border coord but I realized it was better to just start at a coord
#   and go in the direction until there wasn't any other neighbors.
# - This meant I had to keep track of the direction I was going in for each side.
# - I tried vertical and horizontal which worked for some cases but realized
#   I would need to differentiate between left/right and up/down.
# - Long story short, had some trouble figuring out the logic and more trouble
#   implementing it. Tips for future Ethan: don't be afraid to track all direction
#   not just up/down as one direction and left/right as another.
#
# Very fun one today although I struggled a lot. I'm happy with the solution.
#
# I might enjoy an easier way to handle coords soon. `coord1 + coord2` would be super
# nice for adding coords together. I'll have to look into that soon.

input = open(sys.argv[1]).read().strip()

p1 = 0
p2 = 0

# ---- CODE HERE ---- #

grid = input.split("\n")
scanned_coords = set()


# Check if out of bounds
def oob(coords):
    i, j = coords

    if i < 0 or i >= len(grid):
        return True
    if j < 0 or j >= len(grid[0]):
        return True
    return False


# BFS to find the region of a char
# Returns (coords, perimeter, area, sides)
def bfs(coords, char):
    seen = set([coords])
    queue = [coords]

    border = []
    dir_borders = []  # ("l"|"r"|"u"|"d", (i,j))

    curr = None
    while len(queue) > 0:
        curr = queue.pop(0)

        edges = [
            (curr[0] + 1, curr[1] + 0, "d"),  # Down
            (curr[0] - 1, curr[1] + 0, "u"),  # Up
            (curr[0] + 0, curr[1] + 1, "r"),  # Right
            (curr[0] + 0, curr[1] - 1, "l"),  # Left
        ]

        for e in edges:
            edge = (e[0], e[1])
            dir = e[2]
            if edge in seen:
                continue
            if oob(edge) or grid[edge[0]][edge[1]] != char:
                border.append(edge)
                dir_borders.append((dir, edge))
                continue

            queue.append(edge)
            seen.add(edge)
            scanned_coords.add(edge)

    # print("counting sides of", char, "with border", dir_borders)
    area = len(seen)
    peri = len(border)
    sides = count_sides(dir_borders)
    return (seen, peri, area, sides)


# Count the number of sides based on the borders
# Borders are represented as ("l"|"r"|"u"|"d", (i,j))
# This turns an array of border points into an array of sides.
# Each side has a direction and an array of points. Essentially combining
# the coords of neighboring border points into a side.
def count_sides(dir_borders):
    dbset = set(dir_borders)
    sides = []  # [("l"|"r"|"u"|"d", [(i1,j1),(i2,j2),...]),...]

    seen = set()

    # Look through all borders
    for dir_b in dir_borders:
        dir, coord = dir_b
        i, j = coord

        # Skip if it's already in a side
        if dir_b in seen:
            continue

        # New side
        side = (dir, [])

        # Look + (down or right)
        curr = (i, j)
        while (dir, curr) in dbset:
            side[1].append(curr)
            seen.add((dir, curr))

            # Traverse based on direction
            if dir == "l" or dir == "r":
                i += 1
            else:
                j += 1

            curr = (i, j)

        # Look - (up or left)
        i, j = coord  # NOTE: forgot to reset i,j and that caused a bug
        curr = (i, j)
        while (dir, curr) in dbset:
            side[1].append(curr)
            seen.add((dir, curr))

            # Traverse based on direction
            if dir == "l" or dir == "r":
                i -= 1
            else:
                j -= 1

            curr = (i, j)

        # Add side to array
        sides.append(side)

    # for s in sides:
    #     print(s)
    # print()
    return len(sides)


# For each char in the grid, get stats for region it's in
for i, row in enumerate(grid):
    for j, char in enumerate(row):
        coords = (i, j)

        # If coord was found in a BFS, skip it
        if coords in scanned_coords:
            continue

        # Get stats for region
        region_coords, peri, area, sides = bfs(coords, char)
        # print(char, area, peri, sides)

        # Calculate cost
        p1 += area * peri
        p2 += area * sides


# ------------------- #

print("Part 1:", p1)
print("Part 2:", p2)

to_copy = p1 if p2 == 0 else p2
pyperclip.copy(to_copy)
print(f"Copied {'P1' if p2 == 0 else 'P2'}: \"{to_copy}\"")
