import sys
import re
from functools import reduce
import math
from colorama import Fore

pipes = open(sys.argv[1]).read().strip()

p1 = 0
p2 = 0

# ---- CODE HERE ---- #

pipes = pipes.split("\n")

# Find S
s = None
for row, line in enumerate(pipes):
    for col, char in enumerate(line):
        if char == "S":
            s = (row, col)


def get_positions(pos, found, pipes):
    new_finds = {**found}

    queue = [pos]

    while len(queue) > 0:
        curr = queue[0]
        queue = queue[1:]

        for nr, nc in neighbors(curr[0], curr[1], pipes[curr[0]][curr[1]], pipes):
            if 0 <= nr < len(pipes) and 0 <= nc < len(pipes[0]):
                if (nr, nc) not in new_finds and pipes[nr][nc] in "|-LJ7F":
                    new_finds[(nr, nc)] = new_finds[curr] + 1
                    queue.append((nr, nc))

    return new_finds


def neighbors(row, col, char, pipes):
    match char:
        case "|":
            yield (row - 1, col)
            yield (row + 1, col)
        case "-":
            yield (row, col - 1)
            yield (row, col + 1)
        case "L":
            yield (row - 1, col)
            yield (row, col + 1)
        case "J":
            yield (row - 1, col)
            yield (row, col - 1)
        case "7":
            yield (row, col - 1)
            yield (row + 1, col)
        case "F":
            yield (row, col + 1)
            yield (row + 1, col)
        case "S":
            # for i in [-1, 0, 1]:
            #     for j in [-1, 0, 1]:
            #         if i != 0 or j != 0:
            if pipes[row - 1][col] in "7F|":
                yield (row - 1, col)
            if pipes[row + 1][col] in "LJ|":
                yield (row + 1, col)

            if pipes[row][col - 1] in "FL-":
                yield (row, col - 1)
            if pipes[row][col + 1] in "7J-":
                yield (row, col + 1)


finds = get_positions(s, {s: 0}, pipes)
p1 = max([v for key, v in finds.items()])

# This took me a while. But I understand this solution now so I'm happy taking the help with the row by row and replacement idea.
# Idea: (https://www.reddit.com/r/adventofcode/comments/18evyu9/comment/kcqjmnm/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button)

pipes2 = []
for row, line in enumerate(pipes):
    string = ""
    for col, char in enumerate(line):
        if (row,col) not in finds:
            string += "."
        else:
            string += pipes[row][col]
            
    string = re.sub("F-*7","", string) # Shouldn't toggle in_loop
    string = re.sub("L-*J","", string) # Shouldn't toggle in_loop
    string = re.sub("F-*J","|", string) # Should toggle in_loop
    string = re.sub("L-*7","|", string) # Should toggle in_loop
    
    pipes2.append(string)

in_loop = False
within = set()
for row, line in enumerate(pipes2):
    for col, char in enumerate(line):
        if char == ".":
            if in_loop:
                within.add((row,col))
        elif char != "-":
            in_loop = not in_loop

p2 = len(within)

# Nice prints for p1 or testing
# for row, line in enumerate(pipes2):
#     for col, char in enumerate(line):
#         if (row, col) in finds:
#             # print(finds[(row,col)] % 10, end="")
#             # print("X", end="")
#             print(Fore.CYAN, end="")

#         # if pipes[row][col] == ".":
#         if (row, col) in within:
#             print(Fore.RED, end="")

#         print(char, end="")

#         print(Fore.WHITE, end="")
#     print()


# ------------------- #

print("Part 1:", p1)
print("Part 2:", p2)
