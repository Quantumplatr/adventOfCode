import sys
import re
from functools import reduce
import math

input = open(sys.argv[1]).read().strip()

p1 = 0
p2 = 0

# ---- CODE HERE ---- #

lines = input.split("\n")
blocks = [[c for c in l] for l in lines]
best_grid = []

for row in blocks:
    best_grid.append([None] * len(row))


def next_pos(dir, row, col):
    match dir:
        case "N":
            return (row - 1, col)
        case "E":
            return (row, col + 1)
        case "S":
            return (row + 1, col)
        case "W":
            return (row, col - 1)


def recur(blocks, sr, sc, num_so_far, dir, heat):
    
    stack = [(sr, sc, 0, "E", 0),(sr, sc, 0, "S", 0)]
    
    heats = []

    for row in blocks:
        heats.append([None] * len(row))
    
    while len(stack) > 0:
        print(len(stack))
        row, col, num_so_far, dir, heat = stack.pop()
        
        if heats[row][col] is None or heat < heats[row][col]:
            heats[row][col] = heat
            
        options = []

        if dir == "N":
            options = ["N", "E", "W"]
        elif dir == "E":
            options = ["N", "E", "S"]
        elif dir == "S":
            options = ["S", "E", "W"]
        elif dir == "W":
            options = ["N", "S", "W"]

        if num_so_far >= 3:
            options.remove(dir)

        curr_heat = int(blocks[row][col])

        for opt in options:
            nr, nc = next_pos(dir, row, col)

            if not (0 <= nr < len(blocks) and 0 <= nc < len(blocks[0])):
                continue

            next_num = num_so_far + 1 if dir == opt else 0

            stack.append((nr, nc, next_num, opt, heat + curr_heat))


print(blocks)
minimum = recur(blocks, 0, 0, 0, "E", 0)
minimum2 = recur(blocks, 0, 0, 0, "S", 0)

print(minimum, minimum2)

# ------------------- #

print("Part 1:", p1)
print("Part 2:", p2)
