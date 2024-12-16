import sys
import re
from functools import reduce
import math
import pyperclip

# Solved:
# - P1: 2024-12-14
# - P2: 2024-12-15
#
# P1:
# - I'm quite proud of my P1. Placed 469 on day 15!
# - Very, very fun problem imo. Not too difficult either
#   if you're okay with some recursion.
# P2:
# - P2 I had so close to correct but then got stuck in debugging.
#   I had it working on the examples, not as quick as I wanted, but
#   it was working on the examples. And it wasn't working on my input.
#   It was late and I wasn't thinking straight so I gave up for the night.
# - After coming back to it, I solved it super quickly. I had the right idea,
#   just needed to only move recursive boxes if all boxes could move. Basically
#   just need to check if valid move before applying move to boxes.
# - The duplicate code was pretty messy. I could've done that better. I could've
#   potentially represented the boxes better. Maybe track both sides or work with
#   the grid and check neighbors instead of using sets of locations. Idk. Maybe
#   represent a box with a set of points. Idk.
# - Bit messy overall, should've seen my main issue sooner. But I'm happy with the solution.
#   Sad with how long it took me to see the issue though. I was so close to the correct solution.
#   I could've had such a good rank if I saw this sooner. Oh well, super fun problem overall.

input = open(sys.argv[1]).read().strip()

p1 = 0
p2 = 0

# ---- CODE HERE ---- #

warehouse, moves = input.split("\n\n")

warehouse = [[c for c in row] for row in warehouse.split("\n")]
boxes = set()
walls = set()
robot = (-1, -1)

moves = moves.replace("\n", "")

# Parse data out of grid
for i, row in enumerate(warehouse):
    for j, char in enumerate(row):
        if char == "#":
            walls.add((i, j))
        if char == "O":
            boxes.add((i, j))
        if char == "@":
            robot = (i, j)


# Map direction character to (dr,dc)/(di,dj)/direction vector/whatever you want to call it
dirs = {
    "<": (0, -1),
    ">": (0, 1),
    "v": (1, 0),
    "^": (-1, 0),
}


# Pretty print for P1
def pprint():
    for i, row in enumerate(warehouse):
        string = ""
        for j, char in enumerate(row):
            if (i, j) in walls:
                string += "#"
            elif (i, j) in boxes:
                string += "O"
            elif (i, j) == robot:
                string += "@"
            else:
                string += "."
        print(string)


# Out of bounds check for P1
def oob(coords):
    i, j = coords

    if i < 0 or i >= len(warehouse):
        return True
    if j < 0 or j >= len(warehouse[0]):
        return True
    return False


# P1 simulation
# Returns new position when attempting to move
# `pos` in `dir`
def attempt_move(pos, dir):
    di, dj = dir
    i, j = pos

    # New potential i,j
    ni, nj = (i + di, j + dj)

    # Check if out of bounds
    if oob((ni, nj)):
        return (i, j)

    # Check if it would hit a wall
    if (ni, nj) in walls:
        return (i, j)

    # Check if it would push a box
    if (ni, nj) in boxes:
        # Try to move box
        bi, bj = attempt_move((ni, nj), dir)

        # If box didn't move, don't move `pos`
        if bi == ni and bj == nj:
            return (i, j)
        else:
            # If box did move, update box location
            boxes.remove((ni, nj))  # Remove old box location
            boxes.add((bi, bj))  # Add new box location
            return (ni, nj)

    # If all went smoothly, move `pos`
    return (ni, nj)


# Run through P1 simulation
for iter, move in enumerate(moves):
    dir = dirs[move]

    robot = attempt_move(robot, dir)

p1 = sum([i * 100 + j for i, j in boxes])


# --- Part 2 --- #

dw_warehouse = []

dw_walls = set()
dw_boxes = set()
robot2 = (-1, -1)

# Turn warehouse into double wide warehouse
for i, row in enumerate(warehouse):
    nr = []
    for j, char in enumerate(row):
        if char == "#":
            nr += ["#", "#"]
        elif char == "O":
            nr += ["[", "]"]
        elif char == "@":
            nr += ["@", "."]
        else:
            nr += [".", "."]
    dw_warehouse.append(nr)

dw_walls = set()
dw_boxes = set()
robot2 = (-1, -1)

# Parse data out of grid
for i, row in enumerate(dw_warehouse):
    nr = []
    for j, char in enumerate(row):
        if char == "#":
            dw_walls.add((i, j))
        elif char == "[":
            dw_boxes.add((i, j))
        elif char == "@":
            robot2 = (i, j)


# Out of bounds check for P2
def oob2(coords):
    i, j = coords

    if i < 0 or i >= len(dw_warehouse):
        return True
    if j < 0 or j >= len(dw_warehouse[0]):
        return True
    return False


# Pretty print for P2 (double wide)
def pprint2():
    grid = [["." for c in row] for row in dw_warehouse]

    for i, j in dw_walls:
        grid[i][j] = "#"
    for i, j in dw_boxes:
        grid[i][j] = "["
        grid[i][j + 1] = "]"

    i, j = robot2

    grid[i][j] = "\033[93m@\033[0m"

    for row in grid:
        print("".join(row))


# P2 movement. Move `pos` in `dir`.
# Move boxes if `apply_move` is True.
# Returns new position
def attempt_move2(pos, dir, apply_move=True):
    di, dj = dir
    i, j = pos

    # Potential next i,j
    ni, nj = (i + di, j + dj)

    # Don't change if oob
    if oob2((ni, nj)):
        return (i, j)

    # Don't change if would hit wall
    if (ni, nj) in dw_walls:
        return (i, j)

    # Check if it would hit a box (left sid of box or right side of box)
    if (ni, nj) in dw_boxes or (ni, nj - 1) in dw_boxes:
        # Get Original Box I,J
        obi, obj = (ni, nj) if (ni, nj) in dw_boxes else (ni, nj - 1)

        # Whether or not to check each side. Necessary to avoid infinite recursion
        # Only effects horizontal movement. If moving left, only the left side
        # needs to be checked. If the left side can move, so can the right.
        check_left = dir in [(0, -1), (1, 0), (-1, 0)]
        check_right = dir in [(0, 1), (1, 0), (-1, 0)]

        # Check moving both sides of the box
        # Don't move boxes in this check
        # If you did, some recursive calls would work when the whole
        # recursive tree shouldn't. This was the thing that caught me the most
        #
        # Example:
        # If you had `True` for `apply_move` for these two calls below,
        # then this would be the resulting behavior:
        #
        # Initial:
        # ##############
        # ##..........##
        # ##....@.....##
        # ##....[]....##
        # ##...[][]...##
        # ##..[][][]..##
        # ##......##..##
        # ##..........##
        # ##############
        #
        # Move v
        #
        # ##############
        # ##..........##
        # ##....@.....##
        # ##....[]....##
        # ##.....[]...##
        # ##...[].[]..##
        # ##..[][]##..##
        # ##..........##
        # ##############
        #
        # Expected no moves as the robot can't move.
        cant_move = False
        if check_left:
            bi, bj = attempt_move2((obi, obj), dir, False)
            if bi == obi and bj == obj:
                cant_move = True
        if check_right:
            bi2, bj2 = attempt_move2((obi, obj + 1), dir, False)
            if bi2 == obi and bj2 == obj + 1:
                cant_move = True

        # If the box can't move, return
        if cant_move:
            return (i, j)
        else:
            # If can move, and should apply move, move boxes
            if apply_move:
                # Move recursively
                if check_left:
                    bi, bj = attempt_move2((obi, obj), dir, True)
                if check_right:
                    bi2, bj2 = attempt_move2((obi, obj + 1), dir, True)

                # Move box in this function call
                dw_boxes.remove((obi, obj))  # Remove old box location
                dw_boxes.add((obi + di, obj + dj))  # Add new box location
            return (ni, nj)  # Return new position

    # If all goes smoothly, new position
    return (ni, nj)


# Run through P2 simulation
for iter, move in enumerate(moves):
    dir = dirs[move]

    robot2 = attempt_move2(robot2, dir)

p2 = sum([i * 100 + j for i, j in dw_boxes])


# ------------------- #

print("Part 1:", p1)
print("Part 2:", p2)

to_copy = p1 if p2 == 0 else p2
pyperclip.copy(to_copy)
print(f"Copied {'P1' if p2 == 0 else 'P2'}: \"{to_copy}\"")
