import sys
from functools import reduce

input = open(sys.argv[1]).read().strip()

# input = "^v"
# input = "^>v<"
# input = "^v^v^v^v^v""

p1 = 0
p2 = 0

# ---- CODE HERE ---- #

houses1 = {
    "0,0": 1
}

houses2 = {
    "0,0": 1
}

x1 = 0
y1 = 0

x2_s = 0
y2_s = 0

x2_r = 0
y2_r = 0

for i, char in enumerate(input):
    is_santa_move = i % 2 == 0
    
    match char:
        case 'v':
            y1 -= 1
            
            if is_santa_move: 
                y2_s -= 1
            else:
                y2_r -= 1
        case '^':
            y1 += 1
            
            if is_santa_move: 
                y2_s += 1
            else:
                y2_r += 1
        case '>':
            x1 += 1
            
            if is_santa_move: 
                x2_s += 1
            else:
                x2_r += 1
        case '<':
            x1 -= 1
            
            if is_santa_move: 
                x2_s -= 1
            else:
                x2_r -= 1
            
    pos1 = f"{x1},{y1}"
        
    if pos1 in houses1:
        houses1[pos1] += 1
    else:
        houses1[pos1] = 1
        
    pos2 = f"{x2_s},{y2_s}" if is_santa_move else f"{x2_r},{y2_r}"
    
    if pos2 in houses2:
        houses2[pos2] += 1
    else:
        houses2[pos2] = 1
        
p1 = len(houses1)
p2 = len(houses2)

# ------------------- #

print(p1, p2)