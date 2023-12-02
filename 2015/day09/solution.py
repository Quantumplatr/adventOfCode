import sys
from functools import reduce

input = open(sys.argv[1]).read().strip()

p1 = 0
p2 = 0

# ---- CODE HERE ---- #


def get_shortest_from(dists, from_pos, visited, so_far) -> int:
    locations = list(dists.keys())
    not_visited = [loc for loc in locations if loc not in visited and loc != from_pos]

    new_visited = set([from_pos]).union(visited)

    if len(not_visited) == 0:
        return so_far
    else:
        paths = [
            get_shortest_from(
                dists, to_pos, new_visited, so_far + dists[from_pos][to_pos]
            )
            for to_pos in not_visited
        ]
        return min(paths)


def get_longest_from(dists, from_pos, visited, so_far) -> int:
    locations = list(dists.keys())
    not_visited = [loc for loc in locations if loc not in visited and loc != from_pos]

    new_visited = set([from_pos]).union(visited)

    if len(not_visited) == 0:
        return so_far
    else:
        paths = [
            get_longest_from(
                dists, to_pos, new_visited, so_far + dists[from_pos][to_pos]
            )
            for to_pos in not_visited
        ]
        return max(paths)


dists = {}  # eg: { a: {b: 10}, b: {a: 10} }

for line in input.split("\n"):
    from_pos, _, to_pos, _, dist = line.split(" ")

    # Ensure mappings in dists
    if from_pos not in dists:
        dists[from_pos] = {}
    if to_pos not in dists:
        dists[to_pos] = {}

    dists[from_pos][to_pos] = int(dist)
    dists[to_pos][from_pos] = int(dist)


p1 = min([get_shortest_from(dists, pos, set(), 0) for pos in list(dists.keys())])
p2 = max([get_longest_from(dists, pos, set(), 0) for pos in list(dists.keys())])

# ------------------- #

print(p1, p2)
