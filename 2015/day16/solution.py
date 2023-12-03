import sys
from functools import reduce

input = open(sys.argv[1]).read().strip()

p1 = 0
p2 = 0

# ---- CODE HERE ---- #

CORRECT = {
    "children": 3,
    "cats": 7,
    "samoyeds": 2,
    "pomeranians": 3,
    "akitas": 0,
    "vizslas": 0,
    "goldfish": 5,
    "trees": 3,
    "cars": 2,
    "perfumes": 1,
}

sues = {}

# --- Parse --- #

for line in input.split("\n"):
    sue, info = line.split(": ", 1)
    sue = int(sue.split(" ")[1])

    sues[sue] = {}

    for stat in info.split(", "):
        key, value = stat.split(": ")
        value = int(value)

        sues[sue][key] = value

# --- Go through Sues --- #

valid_sues = set(sues.keys())

for sue, info in sues.items():
    for key, value in info.items():
        if CORRECT[key] != value:
            valid_sues.remove(sue)
            break

p1 = valid_sues.pop()

# --- Go again for p2 --- #

valid_sues = set(sues.keys())

for sue, info in sues.items():
    for key, value in info.items():
        correct_val = CORRECT[key]

        if key in ["cats", "trees"]:
            if value <= correct_val:
                valid_sues.remove(sue)
                break
        elif key in ["pomeranians", "goldfish"]:
            if value >= correct_val:
                valid_sues.remove(sue)
                break
        elif correct_val != value:
            valid_sues.remove(sue)
            break

p2 = valid_sues.pop()

# ------------------- #

print(p1, p2)
