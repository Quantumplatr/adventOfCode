import sys
from functools import reduce

input = open(sys.argv[1]).read().strip()

# input = "turn on 0,0 through 2,2\ntoggle 2,2, through 3,3"

p1 = 0
p2 = 0

# ---- CODE HERE ---- #

size = 1000
lights1 = [[False for _ in range(size)] for _ in range(size)]
lights2 = [[0 for _ in range(size)] for _ in range(size)]

for instr in input.split("\n"):
    modes = ["turn on", "toggle", "turn off"]
    
    mode = None
    
    for i, m in enumerate(modes):
        if instr.startswith(m):
            mode = m
            instr = instr[len(m) + 1:] # +1 for space
            
            
    pos1, _, pos2 = instr.split(" ")
    
    pos1 = {
        "x": int(pos1.split(",")[0]),
        "y": int(pos1.split(",")[1]),
    }
    pos2 = {
        "x": int(pos2.split(",")[0]),
        "y": int(pos2.split(",")[1]),
    }
    
    # Loop through positions
    for i in range(pos1["x"], pos2["x"] + 1):
        for j in range(pos1["y"], pos2["y"] + 1):
            
            if mode == "turn on":
                lights1[j][i] = True
                lights2[j][i] += 1
            if mode == "turn off":
                lights1[j][i] = False
                lights2[j][i] -= 1
                if lights2[j][i] < 0:
                    lights2[j][i] = 0
            if mode == "toggle":
                lights1[j][i] = not lights1[j][i]
                lights2[j][i] += 2
                
        
    # for row in lights:
    #     print(" ".join(["1" if light else "0" for light in row]))
        
    # print()

sums = [sum(row) for row in lights1]
sum_of_sums = sum(sums)
p1 = sum_of_sums

sums = [sum(row) for row in lights2]
sum_of_sums = sum(sums)
p2 = sum_of_sums


# ------------------- #

print(p1, p2)