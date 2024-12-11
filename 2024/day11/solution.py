import sys
import re
from functools import reduce
import math
import pyperclip

# Solved: 2024-12-10
# Things to Improve:
# - Pretty happy with P1. Could've coded it faster but took my time
#   with making sure I understood the problem. Not much to improve other than
#   typing speed I guess
# - P2 I took a second to solve. I initially tried to split it in half and blink each half.
#   I knew pretty quick I would need to cache something. Once I figured out to make the
#   recursive function do `Value, Blinks -> Stones From Value`, I had the solution pretty
#   quick. I did miss that the state needed to match the cache key better. I originally
#   did the cache key as `(num)` not `(num,num_blinks)` and that didn't work right.
# - Overall, I'm pretty happy. Just rusty on my memoization (or whatever it's called) and recursion.

input = open(sys.argv[1]).read().strip()

p1 = 0
p2 = 0

# ---- CODE HERE ---- #


# Used for P1
def blink(nums):
    new_nums = []

    # For each number, add output
    for num in nums:
        # 0 -> 1
        if num == 0:
            new_nums.append(1)
        # "AAABBB" -> "AAA", "BBB" (even digits split in half)
        elif len(str(num)) % 2 == 0:
            str_num = str(num)
            left = str_num[: int(len(str_num) / 2)]
            right = str_num[int(len(str_num) / 2) :]
            new_nums.append(int(left))
            new_nums.append(int(right))
        # n -> 2024n
        else:
            new_nums.append(num * 2024)

    return new_nums


# Cache: (value, blinks left)
seen_recur = {}


# Used in P2
# Returns number of resulting stones from blinking `num_blinks` times
# from the value `num`
def recursive_blink(num, num_blinks):
    # Base case
    if num_blinks == 0:
        return 1

    # Check cache
    if (num, num_blinks) in seen_recur:
        return seen_recur[(num, num_blinks)]

    # Recurse cases
    total = 0
    if num == 0:
        total += recursive_blink(1, num_blinks - 1)
    elif len(str(num)) % 2 == 0:
        str_num = str(num)
        left = str_num[: int(len(str_num) / 2)]
        right = str_num[int(len(str_num) / 2) :]
        total += recursive_blink(int(left), num_blinks - 1)
        total += recursive_blink(int(right), num_blinks - 1)
    else:
        total += recursive_blink(num * 2024, num_blinks - 1)

    # Add to cache
    seen_recur[(num, num_blinks)] = total

    return total


# Parse
nums = [int(n) for n in re.findall(r"(\d+)", input)]

# Number of blinks to do (could've used args)
num_blinks = 75

# --- P1 --- #
# curr = nums
# for i in range(num_blinks):
#     curr = blink(curr)
# p1 = len(curr)

# --- P2 --- #
p2 = sum([recursive_blink(n, num_blinks) for n in nums])

# ------------------- #

print("Part 1:", p1)
print("Part 2:", p2)

to_copy = p1 if p2 == 0 else p2
pyperclip.copy(to_copy)
print(f"Copied {'P1' if p2 == 0 else 'P2'}: \"{to_copy}\"")
