import sys
import re
from functools import reduce
import math
import pyperclip

input = open(sys.argv[1]).read().strip()

p1 = 0
p2 = 0

# ---- CODE HERE ---- #

# TODO: solve problem <(• •<)

# ------------------- #

print("Part 1:", p1)
print("Part 2:", p2)

to_copy = p1 if p2 == 0 else p2
pyperclip.copy(to_copy)
print(f"Copied {"P1" if p2 == 0 else "P2"}: \"{to_copy}\"")
