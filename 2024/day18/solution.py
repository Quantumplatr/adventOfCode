import sys
import re
from functools import reduce
import math
import pyperclip
import heapq

input = open(sys.argv[1]).read().strip()

p1 = 0
p2 = 0

# ---- CODE HERE ---- #

width, height = [int(n) for n in sys.argv[2:4]]
num_fall = int(sys.argv[4])

points = [(int(x), int(y)) for x, y in re.findall(r"(\d+),(\d+)", input)]


def pprint(points):
    for i in range(height):
        for j in range(width):
            print("#" if (j, i) in points else ".", end="")
        print()


# Check out of bounds
def oob(coords):
    i, j = coords

    if i < 0 or i >= height:
        return True
    if j < 0 or j >= width:
        return True
    return False


dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]


def path(points, start, end):
    dist = {}
    prev = {}

    dist[start] = 0
    q = [(dist[start], start)]
    for y in range(height):
        for x in range(width):
            if (x, y) not in points:
                heapq.heappush(q, (math.inf, (x, y)))
                dist[(x, y)] = math.inf

    while len(q) > 0:
        # min_dist = min([v for k, v in dist.items() if k in q])
        # key = None
        # for k, v in dist.items():
        #     if v == min_dist and k in q:
        #         key = k
        #         break

        # print({k: v for k, v in dist.items() if k in q}, key)
        # print(q)
        # print(q.index(key))

        # u = q.pop(q.index(key))  # TODO: make pqueue
        u = heapq.heappop(q)

        ux, uy = u[1]

        for dir in dirs:
            dx, dy = dir

            nx, ny = (ux + dx, uy + dy)

            if oob((nx, ny)):
                continue

            if (nx, ny) not in q:
                continue

            alt = dist[(ux, uy)] + 1
            if alt < dist[(nx, ny)]:
                # remove old value
                q.remove((dist[(nx, ny)], (nx, ny)))

                dist[(nx, ny)] = alt
                heapq.heappush(q, (alt, (nx, ny)))

                prev[(nx, ny)] = (ux, uy)

    return dist, prev


def bfs(points, start, end):
    seen = {}

    q = [(0, 0)]

    while len(q) > 0:
        curr = q.pop(0)
        cx, cy = curr

        if curr not in seen:
            seen[curr] = 0

        for dir in dirs:
            dx, dy = dir

            nx, ny = (cx + dx, cy + dy)
            nxt = (nx, ny)

            if oob(nxt):
                continue

            if nxt in points:
                continue

            if nxt in seen:
                if seen[nxt] <= seen[curr] + 1:
                    continue
                else:
                    seen[nxt] = seen[curr] + 1

            q.append(nxt)

            seen[nxt] = seen[curr] + 1

    return seen


def bfs2(points, start, end):
    seen = set()
    q = [start]

    while len(q) > 0:
        # print(len(seen), len(q))
        # print(len(q))
        curr = q.pop(0)
        cx, cy = curr

        if curr == end:
            return True

        seen.add(curr)

        for dir in dirs:
            dx, dy = dir

            nx, ny = (cx + dx, cy + dy)
            nxt = (nx, ny)

            if oob(nxt) or nxt in points:
                continue

            if nxt in seen:
                continue

            seen.add(nxt)

            q.append(nxt)

    return False


# dist, prev = path(points[:num_fall], (0, 0), (width - 1, height - 1))
# print(dist)
# p1 = dist[(width - 1, height - 1)]

# pprint(points[:num_fall])
# output = bfs(points[:num_fall], (0, 0), (width - 1, height - 1))
# print(output)
# print(output[(width - 1, height - 1)])


max_p = len(input.split("\n"))
min_p = num_fall
curr_p = int((max_p + min_p) / 2)

while curr_p != min_p:
    print(curr_p)
    if bfs2(points[:curr_p], (0, 0), (width - 1, height - 1)):
        min_p = curr_p
    else:
        max_p = curr_p

    curr_p = int((max_p + min_p) / 2)

print(bfs2(points[: curr_p + 1], (0, 0), (width - 1, height - 1)))
p2 = points[curr_p]

# ------------------- #

print("Part 1:", p1)
print("Part 2:", p2)

to_copy = p1 if p2 == 0 else p2
pyperclip.copy(to_copy)
print(f"Copied {'P1' if p2 == 0 else 'P2'}: \"{to_copy}\"")
