import sys
import re
from functools import reduce
import math


input = open(sys.argv[1]).read().strip()

p1 = 0
p2 = 0

curr = 50

lines = input.split("\n")
for line in lines:
    dir, num = re.findall(r"(.)(\d+)", line)[0]
    num = int(num)

    # Count any full loops separately
    # to make it easy
    if num > 100:
        p2 += int(num / 100)
        num = num % 100

    prev = curr  # Track prev
    curr += num * (-1 if dir == "L" else 1)  # Apply change
    temp = curr  # Track before mod
    curr = curr % 100  # Mod to keep in [0,99]

    # P1 is if at 0, count
    if curr == 0:
        p1 += 1

    # P2 is if *crossing* 0, count
    # - Not counted if prev was 0
    # - Counted if landing on 0
    # - Counted if mod changed value (e.g. -5 -> 95 means we crossed 0)
    if prev != 0:
        if temp != curr or curr == 0:
            p2 += 1

print(p1)
print(p2)
