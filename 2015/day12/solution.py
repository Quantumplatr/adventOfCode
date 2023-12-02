import sys
import re
from functools import reduce
import json

input = open(sys.argv[1]).read().strip()

p1 = 0
p2 = 0

# ---- CODE HERE ---- #

# --- P1 --- #

tokens = re.split("\[|\]|{|}|\"|,|:", input)

total = 0
for token in tokens:
    if token.isnumeric():
        total += int(token)
        
    if len(token) > 0 and token[0] == "-" and token[1:].isnumeric():
        total -= int(token[1:])

p1 = total

# --- P2 --- #

def get_sum(data) -> int:
    
    if isinstance(data, list):
        return sum([get_sum(item) for item in data])
    elif isinstance(data, int):
        return data
    elif isinstance(data, dict):
        total = 0
        for key, value in data.items():
            if value == "red":
                return 0
            
            total += get_sum(value)
        return total
    else:
        return 0


data = json.loads(input)

p2 = get_sum(data)


# ------------------- #

print(p1, p2)