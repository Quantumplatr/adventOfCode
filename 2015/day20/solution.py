import sys
import re
from functools import reduce
import math
from itertools import chain, combinations

input = open(sys.argv[1]).read().strip()

p1 = 0
p2 = 0

# ---- CODE HERE ---- #

input = int(input)


def get_factorization(num):
    factors = [1]
    curr = num
    while curr != 1:
        for consider in range(2, curr + 1):
            if abs((curr / consider) - int(curr / consider)) <= 0.0001:
                factors.append(consider)
                curr = int(curr / consider)
                break

    return factors


def get_factors(num):
    factors = set()

    for i in range(1, int(num**0.5) + 1):
        if num % i == 0:
            factors.add(i)
            factors.add(int(num / i))

    return factors


# --- P1 --- #

h = 1
while True:

    fac = get_factors(h)

    pres = 10 * sum(fac)

    if pres >= input:
        p1 = h
        break

    h += 1

# --- P2 --- #

# There's probably some nice math here to make it easier but I don't remember much from number theory
h = 1
while True:
    fac = get_factors(h)

    pres = sum([f * 11 for f in fac if h / f <= 50])

    if pres >= input:
        p2 = h
        break

    h += 1

# ------------------- #

print("Part 1:", p1)
print("Part 2:", p2)
