import sys
import re
from functools import reduce
import math
import pyperclip

# Solved: 2024-12-07
# Things I could improve:
# - I had the concept for the solution pretty quick
# - I got really caught up on edge cases. I had a lot of off by 1 with
#   the example input. I think it was just handling the overlaps
# - Another issue was that I was comparing a point with itself (e.g. looking at n[i:] instead of n[i+1:])
#   so I was guaranteed to overcount since every node made two antinodes on itself
# - I also missed that in P2, antinodes CAN appear on a node
# - Anyway, to improve: be more thorough on understanding the problem and what edge cases might be
#   and be more careful of where they might show up in code like what two things I'm comparing

# TODO: clean up / comment this file
# TODO: add `oob` to template? maybe make my own library?

input = open(sys.argv[1]).read().strip()

p1 = 0
p2 = 0

# ---- CODE HERE ---- #


# input = re.sub(r"[^i\.\n]", ".", input)
g = input.split("\n")

nodes = {}


def oob(coords):
    i, j = coords

    if i < 0 or i >= len(g):
        return True
    if j < 0 or j >= len(g[0]):
        return True
    return False


def get_antis(a, b):
    i1, j1 = a
    i2, j2 = b

    # if i1 == i2 and j1 == j2:
    #     return []

    diff = (i1 - i2, j1 - j2)

    p1 = (i1 + diff[0], j1 + diff[1])
    p2 = (i2 - diff[0], j2 - diff[1])

    ps = []
    if not oob(p1):
        ps.append(p1)
    if not oob(p2):
        ps.append(p2)

    return ps


def get_antis2(a, b):
    i1, j1 = a
    i2, j2 = b

    # if i1 == i2 and j1 == j2:
    #     return []

    diff = (i1 - i2, j1 - j2)

    fore = (i1, j1)
    back = (i1, j1)

    ps = []
    while not oob(back):
        ps.append(back)
        back = (back[0] + diff[0], back[1] + diff[1])
    while not oob(fore):
        ps.append(fore)
        fore = (fore[0] - diff[0], fore[1] - diff[1])

    return ps


all_ps = set()
for i, r in enumerate(g):
    for j, char in enumerate(r):
        if char == ".":
            continue
        if char not in nodes:
            nodes[char] = []

        all_ps.add((i, j))
        nodes[char].append((i, j))


all_antis = set()
all_antis_arr = []
for key in nodes:
    n = nodes[key]
    for i, a in enumerate(n):
        for j, b in enumerate(n[i + 1 :]):
            antis = get_antis2(a, b)

            for p in antis:
                # if p not in all_ps:
                all_antis.add(p)
                all_antis_arr.append(p)
# p1 = len(all_antis_arr)
p1 = len(all_antis)


print(nodes)
print(all_antis)

g2 = [[c for c in r] for r in g]
for a in all_antis:
    i, j = a
    if (i, j) not in all_ps:
        g2[i][j] = "#"

for r in g2:
    print("".join(r))

print(len(all_ps))

# ------------------- #

print("Part 1:", p1)
print("Part 2:", p2)

to_copy = p1 if p2 == 0 else p2
pyperclip.copy(to_copy)
print(f"Copied {'P1' if p2 == 0 else 'P2'}: \"{to_copy}\"")
