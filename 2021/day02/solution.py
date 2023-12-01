import sys
from functools import reduce

input = open(sys.argv[1]).read().strip()

p1 = 0
p2 = 0

# ---- CODE HERE ---- #

lines = input.split("\n")

horiz = 0
depth1 = 0
depth2 = 0

aim = 0

for line in lines:
    dir, num = line.split(" ")
    
    match dir:
        case "forward":
            horiz += int(num)
            depth2 += aim * int(num)
        case "down":
            depth1 += int(num)
            aim += int(num)
        case "up":
            depth1 -= int(num)
            aim -= int(num)
            
# print(horiz, depth1)
# print(horiz, depth2)

p1 = horiz * depth1
p2 = horiz * depth2

# ------------------- #

print(p1, p2)