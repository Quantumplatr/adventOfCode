import sys
import re
from functools import reduce
import math
import pyperclip

input = open(sys.argv[1]).read().strip()

p1 = 0
p2 = 0

# ---- CODE HERE ---- #

grid = [[c for c in r] for r in input.split("\n")]

obstacles = set()
guard = (-1, -1)

dir_arr = ">v<^"
dirs = {
    ">": (0, 1),
    "<": (0, -1),
    "^": (-1, 0),
    "v": (1, 0),
}
dir = (0, 0)
dir_char = ""

for i, row in enumerate(grid):
    for j, char in enumerate(row):
        if char in "<>^v":
            guard = (i, j)
            dir = dirs[char]
            dir_char = char
        if char == "#":
            obstacles.add((i, j))

seen = set()


def oob(coords):
    i, j = coords

    if i < 0 or i >= len(grid):
        return True
    if j < 0 or j >= len(grid[0]):
        return True
    return False


seen.add(guard)
print(input)
print()
print(obstacles)
print(guard)


for_loop = set()
while True:
    next = (guard[0] + dir[0], guard[1] + dir[1])

    # Check everything to the right. if anything is seen,
    # add next to for_loop

    rdir_index = dir_arr.index(dir_char)
    rdir_index = (rdir_index + 1) % len(dir_arr)
    rdir_char = dir_arr[rdir_index]
    rdir = dirs[rdir_char]
    rguard = (guard[0], guard[1])

    while True:
        rnext = (rguard[0] + rdir[0], rguard[1] + rdir[1])

        if oob(rnext):
            break

        if grid[rnext[0]][rnext[1]] == "#":
            for_loop.add(next)
            print(next)
            break

        rguard = rnext

    # if next in seen:
    #     nextnext = (next[0] + dir[0], next[1] + dir[1])
    #     if not oob(nextnext):
    #         for_loop.add(nextnext)

    if oob(next):
        break

    if next in obstacles:
        dir_index = dir_arr.index(dir_char)
        dir_index = (dir_index + 1) % len(dir_arr)
        dir_char = dir_arr[dir_index]
        dir = dirs[dir_char]
        continue

    grid[guard[0]][guard[1]] = "X"
    guard = next
    grid[guard[0]][guard[1]] = dir_char
    print("\n".join(["".join(r) for r in grid]))
    print()

    seen.add(guard)

p1 = len(seen)
p2 = len(for_loop)

# ------------------- #

print("Part 1:", p1)
print("Part 2:", p2)

to_copy = p1 if p2 == 0 else p2
pyperclip.copy(to_copy)
print(f"Copied {'P1' if p2 == 0 else 'P2'}: \"{to_copy}\"")
