import sys
import re
from functools import reduce
from numpy import prod
from 

input = open(sys.argv[1]).read().strip()

p1 = 0
p2 = 0

# ---- CODE HERE ---- #

lines = input.split("\n")
times = [int(v) for v in re.findall(r"(\d+)", lines[0])]
dists = [int(v) for v in re.findall(r"(\d+)", lines[1])]


def get_time(accel_time, move_time):
    return accel_time * move_time

wins = [0] * len(times)

for i in range(len(times)):
    available_time = times[i]
    to_beat = dists[i]
    
    for accel_time in range(available_time + 1):
        time = get_time(accel_time, available_time - accel_time)
        
        if time > to_beat:
            wins[i] += 1
     
           
p1 = 1
for win in wins:
    p1 *= win
    

#  ---- P2 ---- #

time = int("".join([str(n) for n in times]))
dist = int("".join([str(n) for n in dists]))

wins2 = 0

for accel_time in range(time + 1):
    t = get_time(accel_time, time - accel_time)
    
    if t > dist:
        wins2 += 1

p2 = wins2


# ------------------- #

print(p1, p2)