import sys
from functools import reduce

input = open(sys.argv[1]).read().strip()

p1 = 0
p2 = 0

# ---- CODE HERE ---- #


def look_and_say(pat: str) -> str:
    res = ""

    i = 0
    while i < len(pat):
        char = pat[i]
        count = 0

        while i < len(pat) and pat[i] == char:
            count += 1
            i += 1

        res += str(count) + char

    return res

curr = input
for i in range(40):
    curr = look_and_say(curr)
p1 = len(curr)

curr = input
for i in range(50):
    curr = look_and_say(curr)
p2 = len(curr)

# ------------------- #

print(p1, p2)
