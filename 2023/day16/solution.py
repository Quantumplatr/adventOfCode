import sys
import re
from functools import reduce
import math

input = open(sys.argv[1]).read().strip()

p1 = 0
p2 = 0

# ---- CODE HERE ---- #


def next_pos(dir, row, col):
    match dir:
        case "N":
            return (row - 1, col)
        case "E":
            return (row, col + 1)
        case "S":
            return (row + 1, col)
        case "W":
            return (row, col - 1)


def print_energized(mirrors, energized):
    for row, line in enumerate(mirrors):
        for col, char in enumerate(line):
            print("#" if (row, col) in energized else ".", end="")
        print()


def move(start_row, start_col, start_dir, mirrors):
    energized = {}
    stack = [(start_row, start_col, start_dir)]

    # Move through stack
    while len(stack) > 0:
        # Current position and dir
        row, col, dir = stack.pop()

        # If not been here, energize
        if (row, col) not in energized:
            energized[(row, col)] = set()

        # If been here and in same dir, short circuit
        if dir in energized[(row, col)]:
            continue

        # Add dir to energized set
        energized[(row, col)].add(dir)

        # Get next pos
        nr, nc = next_pos(dir, row, col)

        # If next pos OOB, skip
        if not (0 <= nr < len(mirrors) and 0 <= nc < len(mirrors[0])):
            continue

        # Next char
        n_char = mirrors[nr][nc]

        # Action based on next char
        match n_char:
            # Continue to next pos in same dir
            case ".":
                stack.append((nr, nc, dir))

            # If perpendicular, split
            # If parallel, continue in same dir
            case "|":
                if dir in ["E", "W"]:
                    stack.append((nr, nc, "N"))
                    stack.append((nr, nc, "S"))
                else:
                    stack.append((nr, nc, dir))

            # If perpendicular, split
            # If parallel, continue in same dir
            case "-":
                if dir in ["S", "N"]:
                    stack.append((nr, nc, "W"))
                    stack.append((nr, nc, "E"))
                else:
                    stack.append((nr, nc, dir))

            # Continue but change dir based on "bounce"
            case "/":
                match dir:
                    case "N":
                        stack.append((nr, nc, "E"))
                    case "E":
                        stack.append((nr, nc, "N"))
                    case "S":
                        stack.append((nr, nc, "W"))
                    case "W":
                        stack.append((nr, nc, "S"))

            # Continue but change dir based on "bounce"
            case "\\":
                match dir:
                    case "N":
                        stack.append((nr, nc, "W"))
                    case "E":
                        stack.append((nr, nc, "S"))
                    case "S":
                        stack.append((nr, nc, "E"))
                    case "W":
                        stack.append((nr, nc, "N"))

    # Once stack is empty, we're done
    return energized


# P1 starts from top left going E
mirrors = input.split("\n")
energized = move(0, -1, "E", mirrors)
# print(input)
# print(energized)
# print_energized(mirrors, energized)

p1 = len(energized) - 1  # -1 b/c it counts the starting OOB pos

# --- P2 ---

max_so_far = -1

# Top row
for col in range(len(mirrors[0])):
    e = move(-1, col, "S", mirrors) # Start above row
    max_so_far = max([len(e) - 1, max_so_far])  # -1 b/c it counts the starting OOB pos

# Bottom row
for col in range(len(mirrors[0])):
    e = move(len(mirrors), col, "N", mirrors) # Start below row
    max_so_far = max([len(e) - 1, max_so_far])  # -1 b/c it counts the starting OOB pos

# Left col
for row in range(len(mirrors)):
    e = move(row, -1, "E", mirrors) # Start to left of col
    max_so_far = max([len(e) - 1, max_so_far])  # -1 b/c it counts the starting OOB pos

# Right col
for row in range(len(mirrors)):
    e = move(row, len(mirrors[0]), "E", mirrors) # Start to right of col
    max_so_far = max([len(e) - 1, max_so_far])  # -1 b/c it counts the starting OOB pos

# P2 is max possible energized count
p2 = max_so_far

# ------------------- #

print("Part 1:", p1)
print("Part 2:", p2)
