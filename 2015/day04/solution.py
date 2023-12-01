import sys
from functools import reduce
import hashlib

input = open(sys.argv[1]).read().strip()

# input = "abcdef" # Expects 609043

p1 = 0
p2 = 0

# ---- CODE HERE ---- #

i = 0
hex = ""
while not hex.startswith("00000"): 

    hash = hashlib.md5((input + str(i)).encode())
    hex = hash.hexdigest()

    i += 1
    
p1 = i - 1

i = 0
hex = ""
while not hex.startswith("000000"): 

    hash = hashlib.md5((input + str(i)).encode())
    hex = hash.hexdigest()

    i += 1
    
p2 = i - 1

# ------------------- #

print(p1, p2)