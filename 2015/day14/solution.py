import sys
from functools import reduce

input = open(sys.argv[1]).read().strip()

p1 = 0
p2 = 0

TOTAL_SEC = 2503

# ---- CODE HERE ---- #

all_deer = {}

for line in input.split("\n"):
    tokens = line.split(" ")
    reindeer = tokens[0]
    speed = int(tokens[3])
    duration = int(tokens[6])
    rest = int(tokens[-2])
    
    all_deer[reindeer] = {
        "speed": speed,
        "duration": duration,
        "rest": rest
    }
    
best_dist = None
for deer, stats in all_deer.items():

    time = 0
    dist = 0
    is_resting = False
    
    while time < TOTAL_SEC:
        if is_resting:
            time += stats["rest"]
        else:
            fly_for = min([stats["duration"],TOTAL_SEC-time])
            dist += fly_for * stats["speed"]
            time += fly_for
        is_resting = not is_resting
        
    if best_dist is None or dist > best_dist:
        best_dist = dist
        
p1 = best_dist
            

# --- P2 --- #

for deer, stats in all_deer.items():
    stats["traveled"] = 0
    stats["till_swap"] = stats["duration"]
    stats["is_resting"] = False
    stats["score"] = 0

for sec in range(TOTAL_SEC):
    # Travel
    for deer, stats in all_deer.items():
        if not stats["is_resting"]:    
            stats["traveled"] += stats["speed"]
            
        stats["till_swap"] -= 1
        
        if stats["till_swap"] == 0:
            stats["is_resting"] = not stats["is_resting"]
            stats["till_swap"] = stats["rest"] if stats["is_resting"] else stats["duration"]
        
    # Award points
    farthest = max([stats["traveled"] for deer, stats in all_deer.items()])
    
    for deer, stats in all_deer.items():
        if stats["traveled"] == farthest:
            stats["score"] += 1
    
p2 = max([stats["score"] for deer, stats in all_deer.items()])


# ------------------- #

print(p1, p2)