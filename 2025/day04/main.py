import sys
import re
from functools import reduce
import math

input = open(sys.argv[1]).read().strip()

p1 = 0
p2 = 0

rows = [[c for c in row] for row in input.split('\n')]

def oob(rows, i, j) -> bool:
    return  not (0 <= i < len(rows) and 0 <= j < len(rows[0]))

def count_neighbors(rows,i,j) -> int:
    count = 0
    for di in [-1,0,1]:
        for dj in [-1,0,1]:
            i1 = di + i
            j1 = dj + j
            if oob(rows, i1, j1) or di == dj == 0:
                continue
            cell1 = rows[i1][j1]
            if cell1 == '@':
                count += 1
    return count



points = set()
for i, row in enumerate(rows):
    row = rows[i]
    for j, cell in enumerate(row):
        if cell != "@":
            continue
        points.add((i,j))

        count = count_neighbors(rows, i, j)

        if count < 4:
            p1 += 1

def next_step(rows):
    out = []
    num_accessible = 0
    for i, row in enumerate(rows):
        row = rows[i]
        r_out = []
        for j, cell in enumerate(row):
            if cell != "@":
                r_out.append(cell)
                continue

            count = count_neighbors(rows, i, j)

            if count < 4:
                r_out.append('.')
                num_accessible += 1
            else:
                r_out.append('@')
        out.append(r_out)
    return (out, num_accessible)


curr = -1
while curr != 0:
    rows, curr = next_step(rows)
    p2 += curr



print("Part 1:", p1)
print("Part 2:", p2)
