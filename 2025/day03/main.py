import sys
import re
from functools import reduce
import math

input = open(sys.argv[1]).read().strip()


p1 = 0
p2 = 0
banks = input.split("\n")

# --- Calculating Joltage --- #
# Given a bank (i.e. 9876543211111) turn on `num_batts` amount
# of digits. Joltage is the number created when concatenating
# the batteries (e.g. if 8 and 2 are turned on `82` is the
# joltage). Batteries cannot be reordered
#
# --- Idea --- #
# Go digit by digit. As the number batts/digits is fixed,
# we always want to maximize each digit. Largest first digit
# will always result in the largest number, regardless of
# other digits (e.g. 9XX,XXX > 2XX,XXX). Going by each digit,
# we find the max digit between the previously found digit and
# the last feasible digit. Obviously it has to be after the prev
# digit. And the last feasible digit just means we have to allow
# space for the remaining digits we still need to turn on.
#
# --- Example --- #
# Bank: 818181911112111
# Num Batteries: 10
#
# - First Digit - #
# Search: 818181--------- (9 left at end)
# Find:   8--------------
#
# - Second Digit - #
# Search: -181819-------- (8 left at end)
# Find:   ------9--------
#
# - Third Digit - #
# Search: -------1------- (7 left at end)
# Find:   -------1-------
#
# ...
#
def max_joltage(bank, num_batts: int) -> int:
    num_digit = 1 

    batts = []
    last_index = -1
    while len(batts) < num_batts:
        digits_left = num_batts - num_digit
        lrg = -1
        for i in range(last_index + 1, len(bank) - digits_left):
            batt = bank[i]
            batt = int(batt)
            if batt > lrg:
                lrg = batt
                last_index = i
        batts.append(lrg)
        num_digit += 1
    joltage = "".join([str(b) for b in batts])
    joltage = int(joltage)
    return joltage


mjs = [max_joltage(bank, 2) for bank in banks]
p1 = sum(mjs)
mjs = [max_joltage(bank, 12) for bank in banks]
p2 = sum(mjs)


print("Part 1:", p1)
print("Part 2:", p2)
