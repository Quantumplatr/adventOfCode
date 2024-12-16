import enum
import sys
import re
from functools import reduce
import math
import pyperclip

# Solved: 2024-12-15
# 2567/1412
# 00:37:03/00:49:52
#
# Thoughts
# - Bit dissapointed in my performance on this one. It felt like
#   it should've been an easy, simple search. I think I was just
#   overthinking things and trying to do backtracking too heavily.
#   My solution runs way slower than it feels like a solution
#   should. But it works! I think I need to freshen up on my
#   Dijkstras which is what I should've implemented immediately.
# - I think a lot of what made mine slow might've been the paths
#   and that it just duplicated the paths a ton.

input = open(sys.argv[1]).read().strip()

p1 = 0
p2 = 0

# ---- CODE HERE ---- #

grid = [[c for c in row] for row in input.split("\n")]

dirs = [(0, 1), (-1, 0), (0, -1), (1, 0)]


# Rotate one direction
def rl(dir):
    ind = dirs.index(dir)
    ind += 1
    return dirs[ind % len(dirs)]


# Rotate the other direction
def rr(dir):
    ind = dirs.index(dir)
    ind -= 1
    return dirs[ind % len(dirs)]


# Check out of bounds
def oob(grid, coords):
    i, j = coords

    if i < 0 or i >= len(grid):
        return True
    if j < 0 or j >= len(grid[0]):
        return True
    return False


# Score consts
SCORE_R = 1000
SCORE_M = 1


# Pretty print the grid with the curr position
def pprint(grid, pos):
    for i, row in enumerate(grid):
        for j, char in enumerate(row):
            if (i, j) == pos:
                print("X", end="")
            else:
                print(char, end="")
        print()


# Cache
seen = {}  # (pos, dir): best score so far


# DFS the grid from start to end
# Track scores and paths
# Return (best score, number of points on best paths)
def score(grid, start, end):
    stack = [
        (start, (0, 1), 0, True, set())
    ]  # (pos, dir, curr_score, can_rotate, path)

    paths = {}  # score: [path]
    while len(stack) > 0:
        # Pop stack
        pos, dir, curr_score, can_rotate, path = stack.pop()
        i, j = pos
        di, dj = dir

        # Check cache
        if (pos, dir) in seen:
            cache_score = seen[(pos, dir)]
            if cache_score < curr_score:
                continue
        seen[(pos, dir)] = curr_score

        # End case
        if (i, j) == end:
            # Add path to paths for score
            if curr_score not in paths:
                paths[curr_score] = []
            paths[curr_score].append(path)
            continue

        # Add rotation movements to stack
        if can_rotate:
            # Rotate one way
            stack.append((pos, rl(dir), curr_score + SCORE_R, False, set(path)))
            # Rotate the other way
            stack.append((pos, rr(dir), curr_score + SCORE_R, False, set(path)))

        # Next position
        ni, nj = (i + di, j + dj)
        next = (ni, nj)

        # If moving would not be out of bounds, hit a wall, or be on the path
        if not oob(grid, (ni, nj)) and grid[ni][nj] != "#" and pos not in path:
            next_path = set(path)
            next_path.add(pos)
            stack.append((next, dir, curr_score + SCORE_M, True, next_path))

    # Get best score and paths to reach score
    best_score = min([score for score in paths])
    best_paths = paths[best_score]

    # Condense to set of points on best paths
    on_best = set()
    for path in best_paths:
        for pos in path:
            on_best.add(pos)

    return (best_score, len(on_best) + 1)  # (best score, num points on best paths)


# Find start and end positions
start = (None, None)
end = (None, None)
for i, row in enumerate(grid):
    for j, char in enumerate(row):
        if char == "S":
            start = (i, j)
        if char == "E":
            end = (i, j)

# Run search
p1, p2 = score(grid, start, end)


# ------------------- #

print("Part 1:", p1)
print("Part 2:", p2)

to_copy = p1 if p2 == 0 else p2
pyperclip.copy(to_copy)
print(f"Copied {'P1' if p2 == 0 else 'P2'}: \"{to_copy}\"")
