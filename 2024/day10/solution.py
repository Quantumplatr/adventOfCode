import sys
import re
from functools import reduce
import math
import pyperclip
import numpy as np  # Tested out printing a numpy obj

# Solved: 2024-12-14
# Things to improve:
# - I think I didn't solve it day of
#   b/c I had date night w/ Carsen.
# - Not much to improve! Pretty happy with this one.
# - P1 seemed like a pretty easy BFS and it was
# - P2 seemed like a pretty easy DFS and it was! Just change queue to a stack

input = open(sys.argv[1]).read().strip()

p1 = 0
p2 = 0

# ---- CODE HERE ---- #

grid = [[int(n) for n in re.findall(r"(\d)", line)] for line in input.split("\n")]


# Check out of bounds
def oob(coords):
    i, j = coords

    if i < 0 or i >= len(grid):
        return True
    if j < 0 or j >= len(grid[0]):
        return True
    return False


# BFS from point to all 9s
def bfs_score(i, j):
    if grid[i][j] != 0:
        return 0

    score = 0

    queue = [(i, j)]
    seen = set()
    while len(queue) > 0:
        r, c = queue.pop(0)
        if (r, c) in seen:
            continue
        seen.add((r, c))
        neighbors = [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]

        curr = grid[r][c]

        # Found trail end
        if curr == 9:
            score += 1
            continue

        # Add valid neighbors to queue
        for n in neighbors:
            ni, nj = n

            # Must be in bounds
            if oob((ni, nj)):
                continue

            # Must be 1 height higher
            next = grid[ni][nj]
            if next != curr + 1:
                continue

            queue.append((ni, nj))

    return score


# DFS from point to all 9s
def dfs_rating(i, j):
    if grid[i][j] != 0:
        return 0

    rating = 0

    stack = [(i, j)]

    while len(stack) > 0:
        r, c = stack.pop()

        neighbors = [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]

        curr = grid[r][c]

        # Found trail end
        if curr == 9:
            rating += 1
            continue

        # Add all valid neighbors to stack
        for n in neighbors:
            ni, nj = n

            # Must be in bounds
            if oob((ni, nj)):
                continue

            # Must be 1 height higher
            next = grid[ni][nj]
            if next != curr + 1:
                continue

            stack.append((ni, nj))

    return rating


# Search all trailheads (0s)
for i, row in enumerate(grid):
    for j, curr in enumerate(row):
        if curr == 0:
            p1 += bfs_score(i, j)
            p2 += dfs_rating(i, j)

# ------------------- #

print("Part 1:", p1)
print("Part 2:", p2)

to_copy = p1 if p2 == 0 else p2
pyperclip.copy(to_copy)
print(f"Copied {'P1' if p2 == 0 else 'P2'}: \"{to_copy}\"")
