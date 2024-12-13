import sys
import re
from functools import reduce
import math
import pyperclip

# Solved: 2024-12-12
# Things to improve:
# - Holy shit today was painful. Omfg.
# - Took me a whole half hour to realize it's just linear algebra
# - Took me another 15 mins to solve a system of equations.
# - Fml. Note to self: Catch up on linear algebra. It's not like it's been like 5
#   years at this point or anything.
#
# - I started trying to do backtracking. Turns out that's too slow obviously. Esp
#   for P2.

input = open(sys.argv[1]).read().strip()

p1 = 0
p2 = 0

# ---- CODE HERE ---- #

machines_in = input.split("\n\n")

a_cost = 3
b_cost = 1

seen = {}  # start: (As, Bs)


hits = 0
misses = 0


# My backtracking pain
def get_optimal(start, end, da, db, As, Bs):
    global hits, misses
    # print(start, end, da, db, As, Bs)
    # pa = (start[0] + da[0], start[1] + da[1])
    # pb = (start[0] + db[0], start[1] + db[1])
    pa = (As * da[0], As * da[1])
    pb = (Bs * db[0], Bs * db[1])

    if As == 80:
        print(pa, pb, As, Bs)
    if pa[0] == end[0] and pa[1] == end[1]:
        return (As, Bs)
    if pb[0] == end[0] and pb[1] == end[1]:
        return (As, Bs)

    # print(seen)

    if start in seen:
        # print("cache hit", hits)
        hits += 1
        return seen[start]
    # print("cache miss", misses)
    misses += 1

    if pa[0] > end[0] or pa[1] > end[1]:
        return (None, None)

    if pb[0] > end[0] or pb[1] > end[1]:
        return (None, None)

    a_As, a_Bs = get_optimal(pa, end, da, db, As + 1, Bs)
    b_As, b_Bs = get_optimal(pb, end, da, db, As, Bs + 1)

    if As == 80 and Bs == 34:
        print(start, end, da, db, As, Bs)

    result = (None, None)
    if a_As is None and b_As is not None:
        result = (b_As, b_Bs)
        seen[start] = result
        return result
    if b_As is None and a_As is not None:
        result = (a_As, a_Bs)
        seen[start] = result
        return result
    if a_As is None and b_As is None:
        seen[start] = result
        return result

    a_c = cost(a_As, a_Bs)
    b_c = cost(b_As, b_Bs)

    result = (a_As, a_Bs) if a_c < b_c else (b_As, b_Bs)

    seen[start] = result

    return result


# Solve system of equtions to calculate number of presses needed
def get_optimal2(a, b, end):
    # [ax, bx] x [ num As ] = [ end_x ]
    # [ay, by]   [ num Bs ] = [ end_y ]

    ax, ay = a
    bx, by = b

    ex, ey = end

    # Cramer's rule
    det = ax * by - bx * ay

    det1 = ex * by - bx * ey
    det2 = ax * ey - ex * ay

    na = det1 / det
    nb = det2 / det

    return (na, nb)


# Calculate cost based on number of presses
def cost(As, Bs):
    return As * a_cost + Bs * b_cost


for m in machines_in:
    a_in, b_in, p_in = m.split("\n")

    a = re.findall(r"[XY]\+(\d+)", a_in)
    b = re.findall(r"[XY]\+(\d+)", b_in)
    p = re.findall(r"=(\d+)", p_in)

    a = [int(n) for n in a]
    b = [int(n) for n in b]
    p = [int(n) for n in p]

    # As, Bs = get_optimal((0, 0), p, a, b, 0, 0)
    As, Bs = get_optimal2(a, b, p)

    # P1
    if As == int(As) and Bs == int(Bs):
        p1 += cost(As, Bs)

    # P2
    offset = 10000000000000
    As, Bs = get_optimal2(a, b, (p[0] + offset, p[1] + offset))

    if As == int(As) and Bs == int(Bs):
        p2 += cost(As, Bs)


# ------------------- #

print("Part 1:", int(p1))
print("Part 2:", p2)

to_copy = p1 if p2 == 0 else p2
pyperclip.copy(to_copy)
print(f"Copied {'P1' if p2 == 0 else 'P2'}: \"{to_copy}\"")
