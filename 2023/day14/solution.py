import sys
import re
from functools import reduce
import math

input = open(sys.argv[1]).read().strip()

p1 = 0
p2 = 0

# ---- CODE HERE ---- #

lines = input.split("\n")
spaces = [[c for c in line] for line in lines]

# Roll all "O"s as far as possible in dir
def roll(spaces, dir):
    
    # N/S
    if dir in ["N","S"]:
        order = range(len(spaces)) if dir == "N" else range(len(spaces) -1, -1, -1)
        for col in range(len(spaces[0])):
            for row in order:
                
                char = spaces[row][col]
                
                if char == "O":
                    if dir == "N" and row == 0:
                        continue
                    if dir == "S" and row == len(spaces) - 1:
                        continue
                    
                    i = row
                    diff = -1 if dir == "N" else 1
                    prev = spaces[i + diff][col]
                    while True:
                        
                        # If at stopper (edge or "#"), stop moving
                        if not 0 <= i + diff < len(spaces) or prev != ".":
                            break
                        
                        # Swap
                        spaces[i][col] = prev
                        spaces[i + diff][col] = char
                        
                        # Continue if can
                        i += diff
                        if i + diff >= len(spaces):
                            break
                        prev = spaces[i + diff][col]
                        
    # E/W
    if dir in ["E","W"]:
        order = range(len(spaces[0])) if dir == "W" else range(len(spaces[0]) -1, -1, -1)
        for row in range(len(spaces)):
            for col in order:
                
                char = spaces[row][col]
                
                if char == "O":
                    if dir == "W" and col == 0:
                        continue
                    if dir == "E" and col == len(spaces[0]) - 1:
                        continue
                        
                    i = col
                    diff = -1 if dir == "W" else 1
                    prev = spaces[row][i+diff]
                    while True:
                        
                        # If at stopper (edge or "#"), stop moving
                        if not 0 <= i + diff < len(spaces[0]) or prev != ".":
                            break
                        
                        # Swap
                        spaces[row][i] = prev
                        spaces[row][i + diff] = char
                        
                        # Continue if can
                        i += diff
                        if i + diff >= len(spaces[0]):
                            break
                        prev = spaces[row][i + diff]
                    
    return spaces
                
def north_sup(spaces):
    tot = 0
    for col in range(len(spaces[0])):
        for row in range(len(spaces)):
            
            char = spaces[row][col]
            
            if char == "O":
                tot += len(spaces) - row
            
    return tot

def to_str(spaces):
    return "\n".join(["".join(line) for line in spaces1])

spaces1 = roll(spaces, "N")
            
p1 = north_sup(spaces1)
        
# P2

spaces2 = spaces

dirs = ["N", "W", "S", "E"]
dir_ind = 0
patterns = { to_str(spaces2): 0 }
num_cycles = 1_000_000_000

# Cycle until repeat
for i in range(num_cycles):
    # 1 cycle is all dirs
    for dir in dirs:
        spaces2 = roll(spaces2, dir)
    
    if to_str(spaces2) in patterns:
        break
    else:
        patterns[to_str(spaces2)] = i + 1 # Num cycles done
    
# Calculate where it would end based on length of repeating cycles
repeat_len = i - patterns[to_str(spaces2)] + 1
num_left = num_cycles - i - 1
end_on = num_left % repeat_len + patterns[to_str(spaces2)]

# Get ending state
end_state = None
for pat in patterns:
    if patterns[pat] == end_on:
        end_state = pat
        break

# Get value of ending state
p2 = north_sup([[c for c in line] for line in end_state.split("\n")])

# ------------------- #

print("Part 1:", p1)
print("Part 2:", p2)