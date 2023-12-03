import sys
from functools import reduce

input = open(sys.argv[1]).read().strip()

p1 = 0
p2 = 0

# ---- CODE HERE ---- #

lights = []

for line in input.split("\n"):
    lights.append([char for char in line])


def step(lights, corners_on=False):
    new_lights = [list(row) for row in lights]

    num_row = len(lights)
    num_col = len(lights[0])

    for row in range(num_row):
        for col in range(num_col):
            
            if corners_on and (row,col) in [(0,0),(0,num_col-1),(num_row-1,0),(num_row-1,num_col-1)]:
                new_lights[row][col] = "#"
                continue
            
            nw = lights[row - 1][col - 1] if row - 1 >= 0 and col - 1 >= 0 else "."
            no = lights[row - 1][col + 0] if row - 1 >= 0 else "."
            ne = lights[row - 1][col + 1] if row - 1 >= 0 and col + 1 < num_col else "."
            we = lights[row + 0][col - 1] if col - 1 >= 0 else "."
            ea = lights[row + 0][col + 1] if col + 1 < num_col else "."
            sw = lights[row + 1][col - 1] if row + 1 < num_row and col - 1 >= 0 else "."
            so = lights[row + 1][col + 0] if row + 1 < num_row else "."
            se = (
                lights[row + 1][col + 1]
                if row + 1 < num_row and col + 1 < num_col
                else "."
            )

            neighbors = [nw, no, ne, we, ea, sw, so, se]
            on_count = len([light for light in neighbors if light == "#"])
            
            light = lights[row][col]
            new_light = "."
            
            if light == "#":
                if on_count in [2,3]:
                    new_light = "#"
            else:
                if on_count == 3:
                    new_light = "#"
                    
            new_lights[row][col] = new_light

    return new_lights


def pprint(lights):
    for row in lights:
        print("".join(row))


STEPS = 100


curr = [list(row) for row in lights]
# print("Initial state:")
# pprint(curr)

for i in range(STEPS):
    curr = step(curr)
    
    # print("After",i+1,f"step{'s' if i != 0 else ''}:")
    # pprint(curr)
    # print()
    
p1 = sum([len([1 for light in row if light == "#"]) for row in curr])

# --- p2 --- #

curr = [list(row) for row in lights]
curr[0][0] = "#"
curr[0][-1] = "#"
curr[-1][0] = "#"
curr[-1][-1] = "#"
# print("Initial state:")
# pprint(curr)

for i in range(STEPS):
    curr = step(curr, True)
    
    # print("After",i+1,f"step{'s' if i != 0 else ''}:")
    # pprint(curr)
    # print()

p2 = sum([len([1 for light in row if light == "#"]) for row in curr])

# ------------------- #

print(p1, p2)
