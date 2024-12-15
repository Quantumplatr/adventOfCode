import sys
import re
from functools import reduce
import math
import pyperclip

import msvcrt as m

input = open(sys.argv[1]).read().strip()

p1 = 0
p2 = 0

# ---- CODE HERE ---- #

warehouse, moves = input.split("\n\n")

warehouse = [[c for c in row] for row in warehouse.split("\n")]
boxes = set()
walls = set()
robot = (-1,-1)

moves = moves.replace("\n", "")

for i, row in enumerate(warehouse):
    for j, char in enumerate(row):
        if char == "#":
            walls.add((i,j))
        if char == "O":
            boxes.add((i,j))
        if char == "@":
            robot = (i,j)


dirs = {
    "<": (0,-1),
    ">": (0,1),
    "v": (1,0),
    "^": (-1,0),
}

def pprint():
    for i, row in enumerate(warehouse):
        string = ""
        for j, char in enumerate(row):
            if (i,j) in walls:
                string += "#"
            elif (i,j) in boxes:
                string += "O"
            elif (i,j) == robot:
                string += "@"
            else:
                string += "."
        print(string)


def oob(coords):
    i, j = coords

    if i < 0 or i >= len(warehouse):
        return True
    if j < 0 or j >= len(warehouse[0]):
        return True
    return False

def attempt_move(pos, dir):
    di, dj = dir
    i, j = pos

    ni, nj = (i + di, j + dj)

    if oob(( ni, nj )):
        return (i,j)

    if (ni, nj) in walls:
        return (i,j)

    if (ni, nj) in boxes:
        bi, bj = attempt_move((ni,nj), dir) 

        if bi == ni and bj == nj:
            return (i, j)
        else:
            boxes.remove((ni, nj)) # Remove old box location
            boxes.add((bi, bj)) # Add new box location
            return (ni, nj)
    

    return (ni, nj)




print("initial")
pprint()
print()
for iter, move in enumerate(moves):
    dir = dirs[move]

    robot = attempt_move(robot, dir)

    # print(iter, move)
    # pprint()
    # print()

p1 = sum([i*100 + j for i,j in boxes])



dw_warehouse = []

dw_walls = set()
dw_boxes = set()
robot2 = (-1,-1)

for i, row in enumerate(warehouse):
    nr = []
    for j, char in enumerate(row):
        if char == "#":
            nr += ["#","#"]
        elif char == "O":
            nr += ["[","]"]
        elif char == "@":
            nr += ["@","."]
        else:
            nr += [".","."]
    dw_warehouse.append(nr)

dw_walls = set()
dw_boxes = set()
robot2 = (-1,-1)

for i, row in enumerate(dw_warehouse):
    nr = []
    for j, char in enumerate(row):
        if char == "#":
            dw_walls.add((i,j))
        elif char == "[":
            dw_boxes.add((i,j))
        elif char == "@":
            robot2 = (i,j)

def oob2(coords):
    i, j = coords

    if i < 0 or i >= len(dw_warehouse):
        return True
    if j < 0 or j >= len(dw_warehouse[0]):
        return True
    return False
def pprint2():

    grid = [["." for c in row] for row in dw_warehouse]

    for i,j in dw_walls:
        grid[i][j] = "#"
    for i,j in dw_boxes:
        grid[i][j] = "["
        grid[i][j+1] = "]"

    i,j = robot2

    grid[i][j] = "\033[93m@\033[0m"

    for row in grid:
        print("".join(row))

def attempt_move2(pos, dir):
    # print(pos, dir)
    di, dj = dir
    i, j = pos

    ni, nj = (i + di, j + dj)

    if oob2(( ni, nj )):
        return (i,j)

    if (ni, nj) in dw_walls:
        return (i,j)

    if (ni, nj) in dw_boxes or (ni, nj-1) in dw_boxes:
        # print('found box')
        obi, obj =(ni, nj) if (ni, nj) in dw_boxes else (ni, nj-1)

        check_left = dir in [(0,-1), (1,0), (-1,0)]
        check_right = dir in [(0,1), (1,0), (-1,0)]

        cant_move = False
        
        if check_left:
            bi, bj = attempt_move2((obi, obj), dir) 
            if bi == obi and bj == obj:
                cant_move = True
        if check_right:
            bi2, bj2 = attempt_move2((obi, obj+1), dir) 
            if bi2 == obi and bj2 == obj+1:
                cant_move = True

        if cant_move:
            return (i,j)
        else:
            dw_boxes.remove((obi, obj)) # Remove old box location
            dw_boxes.add((obi+di, obj+dj)) # Add new box location # TODO: confirm
            return (ni, nj)
    

    return (ni, nj)

pprint2()



print("initial")
pprint2()
print()
for iter, move in enumerate(moves):
    dir = dirs[move]

    robot2 = attempt_move2(robot2, dir)

    # print(iter, move)
    # # m.getch()
    # pprint2()
    # print()

print("final")
pprint2()
print()
p2 = sum([i * 100 + j for i,j in dw_boxes])


# ------------------- #

print("Part 1:", p1)
print("Part 2:", p2)

to_copy = p1 if p2 == 0 else p2
pyperclip.copy(to_copy)
print(f"Copied {'P1' if p2 == 0 else 'P2'}: \"{to_copy}\"")
