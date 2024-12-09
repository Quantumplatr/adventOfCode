import sys
import re
from functools import reduce
import math
import pyperclip

# Solved: 2024-12-08
# Things to improve:
# - I just felt slow today. Spent a while making sure I understood the prompt
# - Took a while to parse into a data structure
# - Fairly happy with solution once I had the data structure
# - Messed up the checksum which slowed me down
# - Making the fancy print earlier might've been nice
# - Didn't super rush today but I feel like that's okay with it feeling
#   like an intricate problem

# TODO: cleanup and comment

input = open(sys.argv[1]).read().strip()

p1 = 0
p2 = 0

# ---- CODE HERE ---- #

chunks = []

num_gaps = 0
block = True
for i, d in enumerate(input):
    if block:
        chunks.append((int(i / 2), int(d)))
    else:
        num_gaps += 1
        chunks.append((-1, int(d)))

    block = not block

if chunks[-1][0] == -1:
    chunks = chunks[:-1]


def printc(chunks):
    s = ""
    for c in chunks:
        id = str(c[0]) if c[0] != -1 else "."
        s += id * c[1]
    print(s)


# TODO: turn into P2 function
i = len(chunks) - 1
while i > 0:
    chunk = chunks[i]

    id, size = chunk

    # Skip gaps
    if id == -1:
        i -= 1
        continue

    # Search for fitting gap
    j = 0
    while j < i:
        curr = chunks[j]
        gid, gsize = curr
        if gid != -1:
            j += 1
            continue

        # If fitting gap
        if gsize >= size:
            # Decrease gap size
            chunks[j] = (-1, gsize - size)

            # Insert new chunk
            chunks.insert(j, (id, size))

            # Change moved chunk to gap
            chunks[i + 1] = (-1, size)

            # If emptied gap, remove
            if gsize == size:
                del chunks[j + 1]

            break

        j += 1

    # Next chunk back
    i -= 1

    # printc(chunks)


# TODO: turn into P1 function
#
# i = 0
# printc(chunks)
# while i < len(chunks):
#     chunk = chunks[i]
#
#     id, size = chunk
#
#     if id != -1:
#         i += 1
#         continue
#
#     last = chunks[-1]
#     lid, lsize = last
#
#     if lid == -1:
#         chunks = chunks[:-1]
#         continue
#
#     # Fully replace curr gap
#     if lsize >= size:
#         chunks[i] = (lid, size)
#
#         # Remove last if emptied
#         if lsize == size:
#             chunks = chunks[:-1]
#         # Remove count
#         else:
#             chunks[-1] = (lid, lsize - size)
#
#     # If partial fill,
#     else:
#         # Decrease gap size
#         chunks[i] = (-1, size - lsize)
#
#         # Insert new chunk
#         chunks.insert(i, (lid, lsize))
#
#         # Remove last chunk
#         chunks = chunks[:-1]
#
#         # i += 1
#
#     printc(chunks)
#     i += 1
#
# print(chunks)


def checksum(chunks):
    total = 0
    index = 0
    for i, c in enumerate(chunks):
        id, size = c
        for j in range(size):
            if id != -1:
                total += index * id
            index += 1
    return total


p1 = checksum(chunks)

# ------------------- #

print("Part 1:", p1)
print("Part 2:", p2)

to_copy = p1 if p2 == 0 else p2
pyperclip.copy(to_copy)
print(f"Copied {'P1' if p2 == 0 else 'P2'}: \"{to_copy}\"")
