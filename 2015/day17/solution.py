import sys
from functools import reduce

input = open(sys.argv[1]).read().strip()

p1 = 0
p2 = 0

# ---- CODE HERE ---- #

total = 150

sizes = []

for i, line in enumerate(input.split("\n")):
    sizes.append((i,int(line)))

# Build a set of combos where a combo is a list of indeces into the sizes array
def backtrack(left: int, available: [int], combos: set, combo: list):
    for i, tup in enumerate(available):
        index, size = tup
        new_combo = combo + [index]
        
        if left == size:
            combos.add(frozenset(new_combo))
        elif size < left:
            backtrack(
                left - size,
                available[:i] + available[i + 1 :],
                combos,
                new_combo,
            )
            
    return combos


combos = backtrack(total, sizes, set(), [])
p1 = len(combos)

min_size = min([len(combo) for combo in combos])
count = len([1 for combo in combos if len(combo) == min_size])

p2 = count

# Note: This is a lil slow. Could be improved w/ dynamic programming maybe

# ------------------- #

print(p1, p2)
