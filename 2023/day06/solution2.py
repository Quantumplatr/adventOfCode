import sys
import re
from functools import reduce
import math

input = open(sys.argv[1]).read().strip()

p1 = 0
p2 = 0

# ---- CODE HERE ---- #

lines = input.split("\n")
times = [int(v) for v in re.findall(r"(\d+)", lines[0])]
dists = [int(v) for v in re.findall(r"(\d+)", lines[1])]


def get_num_times(t,b):

    # Solve below and count how many ints are between two sols
    # m := time to move
    # a := time to accel
    # b := time to beat
    # t := time available
    #
    # m * a = b
    # m + a = t
    #
    # solution
    # m**2 - tm + b = 0
    # a = b / m
    #
    # m = (t +- sqrt(t**2 - 4b)) / 2
    # a = b / m
    #
    # Number of different splits between two m or a values should
    
    m1 = (t + (t**2 - 4*b) ** 0.5) / 2
    m2 = (t - (t**2 - 4*b) ** 0.5) / 2
    
    m_max = max([m1,m2])
    m_min = min([m1,m2])
    
    if m_min == int(m_min):
        m_min += 1
    else:
        m_min = math.ceil(m_min)
        
    if m_max == int(m_max):
        m_max -= 1
    else:
        m_max = math.floor(m_max)
    
    m_min = math.floor(m_min)
    m_max = math.ceil(m_max)
    
    
    return m_max - m_min + 1

wins = [0] * len(times)

p1 = 1
for i in range(len(times)):
    t = times[i]
    b = dists[i]
    
    
    
    p1 *= get_num_times(t,b)

    
p2 = 1

t = int("".join([str(n) for n in times]))
b = int("".join([str(n) for n in dists]))

p2 = get_num_times(t,b)



# ------------------- #

print(p1, p2)