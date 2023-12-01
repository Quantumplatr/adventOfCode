import sys
from functools import reduce

input = open(sys.argv[1]).read().strip()

p1 = 0
p2 = 0

# ---- CODE HERE ---- #

lines = input.split("\n")

for line in lines:
    length, width, height = [int(dim) for dim in line.split("x")]

    sa = 2 * (length * width + length * height + width * height)
    extra = (length * width * height) / max(length, width, height)

    ribbon = (
        2 * sum([length, width, height])
        - 2 * max(length, width, height)
        + (length * width * height)
    )

    print(length, width, height)
    print(sa, extra)

    p1 += sa + extra
    p2 += ribbon


# ------------------- #

print(p1, p2)
