import sys
import re
from functools import reduce
import math

input = open(sys.argv[1]).read().strip()

p1 = 0
p2 = 0

# ---- CODE HERE ---- #

def get_diffs(nums):
    
    diffs = [nums]
    
    
    while any([n != 0 for n in diffs[-1]]):
        seq = diffs[-1]
        
        next_diffs = [seq[i+1] - seq[i] for i in range(len(seq)-1)]
        
        diffs.append(next_diffs)
        
    return diffs

def get_next(nums):
    
    diffs = get_diffs(nums)
        
    # for i, d in enumerate(diffs):
    #     print(" " * i + " ".join([str(item) for item in d]))
        
    return sum([diff[-1] for diff in diffs if len(diff) > 0])

def get_prev(nums):
    
    diffs = get_diffs(nums)
    
    # for i, d in enumerate(diffs):
    #     print(" " * i + " ".join([str(item) for item in d]))
    
    prev = 0
    for diff in diffs[::-1]:
        prev = diff[0] - prev
        
    return prev

    

for line in input.split("\n"):
    nums = [int(n) for n in re.findall(r"(-*\d+)", line)]
    
    p1 += get_next(nums)
    
    p2 += get_prev(nums)


# ------------------- #

print("Part 1:", p1)
print("Part 2:", p2)