import sys
from functools import reduce
from itertools import permutations

input = open(sys.argv[1]).read().strip()

p1 = 0
p2 = 0

# ---- CODE HERE ---- #

def get_best(happiness: dict) -> int:
    people = list(happiness.keys())

    best_so_far = None
    for perm in permutations(people):
        net = 0
        for i, person in enumerate(perm):
            neighbor1 = perm[(i+1) % len(perm)]
            neighbor2 = perm[(i-1) % len(perm)]
            
            net += happiness[person][neighbor1]
            net += happiness[person][neighbor2]
            
        if best_so_far is None:
            best_so_far = net
        else:
            best_so_far = max([best_so_far, net])

    return best_so_far

happiness = {}

for line in input.split("\n"):
    tokens = line.split(" ")
    person1 = tokens[0]
    gain_loss = tokens[2]
    amount = tokens[3]
    person2 = tokens[-1][:-1]
    
    if person1 not in happiness:
        happiness[person1] = {}
        
    happiness[person1][person2] = int(amount) * (-1 if gain_loss == "lose" else 1)
    
        
p1 = get_best(happiness)

# --- P2 --- #

# Add me with all happiness values of 0
happiness["me"] = {}
for person in happiness:
    happiness["me"][person] = 0
    happiness[person]["me"] = 0

p2 = get_best(happiness)

# ------------------- #

print(p1, p2)