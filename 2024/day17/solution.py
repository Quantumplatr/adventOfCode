import enum
import sys
import re
from functools import reduce
import math
import pyperclip

input = open(sys.argv[1]).read().strip()

p1 = 0
p2 = 0

# ---- CODE HERE ---- #


registers, program = input.split("\n\n")

a, b, c = [int(n) for n in re.findall(r"(\d+)", registers)]

operations = [int(n) for n in re.findall(r"(\d+)", program)]

pointer = 0


def get_combo(input):
    value = 0
    if input in [0, 1, 2, 3]:
        value = input
    if input == 4:
        value = a
    if input == 5:
        value = b
    if input == 6:
        value = c
    return value


def adv(input):
    global a
    value = get_combo(input)

    a = int(a / pow(2, value))
    return None


def bxl(input):
    global b
    b = b ^ input
    return None


def bst(input):
    global b
    value = get_combo(input) % 8
    b = value
    return None


def jnz(input):
    global a
    global pointer
    if a == 0:
        return None
    else:
        pointer = input
        return None


def bxc(input):
    global b
    global c
    b = b ^ c
    return None


def out(input):
    return get_combo(input) % 8


def bdv(input):
    global b
    value = get_combo(input)

    b = int(a / pow(2, value))
    return None


def cdv(input):
    global c
    value = get_combo(input)

    c = int(a / pow(2, value))
    return None


ops = [
    adv,  # 0
    bxl,  # 1
    bst,  # 2
    jnz,  # 3
    bxc,  # 4
    out,  # 5
    bdv,  # 6
    cdv,  # 7
]

cache = {}  # (pointer,a,b,c) : output

cache_hits = 0


def run(operations):
    global pointer
    global a
    global b
    global c
    global cache_hits
    output = []
    pointer = 0
    positions = {}
    cache_hit = None
    while pointer < len(operations):
        key = (pointer, a, b, c)
        positions[key] = len(output)
        # Check cache
        if key in cache:
            cache_hits += 1
            cache_hit = output + cache[key]
            break
            # print("cache hit")
            cache_hit = key
            # break

        op = operations[pointer]
        input = operations[pointer + 1]
        # print(ops[op].__name__, input)
        res = ops[op](input)
        if res is not None:
            output.append(res)

        # Jump conditions
        if op == 3 and a != 0:
            continue

        pointer += 2

    # print(cache)

    if cache_hit:
        output = cache_hit
    #     pass
    # print(cache_hit, cache[cache_hit])

    # print(output)
    for position in positions:
        # print(output, position, positions)
        unused = positions[position]
        cache[position] = output[unused:]
    # print(cache)

    return output


p1 = ",".join([str(n) for n in run(operations)])
print(p1)


def base_change(n):
    o = 0
    for i, d in enumerate(n):
        o += d * pow(8, i)

    return o


def test(A):
    # return (((A % 8) ^ 5 ^ 6) ^ (A >> ((A % 8) ^ 5))) % 8
    return (((A % 8) ^ 3) ^ (A >> ((A % 8) ^ 5))) % 8


def find(digits):
    global a
    global b
    global c
    global pointer
    if len(digits) == len(operations):
        return digits
    so_far = 0
    for i, d in enumerate(digits):
        so_far += d * pow(8, i)

    digit = len(operations) - 1 - len(digits)

    correct = operations[digit]
    potential = []
    print(digits, base_change(digits), correct)
    for i in range(8):
        a = base_change([i] + digits)
        b = 0
        c = 0
        pointer = 0
        output = run(operations)

        val = test(so_far * 8 + i)
        print(a, output, val)
        if val == correct:
            print("found")
            potential.append(i)

    if len(potential) == 0:
        return None

    for p in potential:
        new_digits = [p] + digits
        result = find(new_digits)
        if result is not None:
            return result

    return None


digits = find([])
p2 = base_change(digits)
print("want", operations)
a = p2
b = 0
c = 0
print("res", run(operations))
print(p2)

exit()

curr = None
i = 1
while True:
    # if i % 10000 == 0:
    #     print(i, len(cache), cache_hits, curr, operations)
    a = i
    b = 0
    c = 0

    curr = run(operations)

    if len(curr) == len(operations):
        all_same = True
        for j, val in enumerate(curr):
            if val != operations[j]:
                all_same = False
                break
        if all_same:
            break

    if len(curr) < len(operations):
        i *= 2
    else:
        i += 1

    if curr[:5] == operations[:5]:
        print(i)


print(cache)
print(len(cache))
p2 = i


# 2,4,1,5,7,5,1,6,0,3,4,2,5,5,3,0
#
# bst(4), bxl(5), cdv(5), bxl(6), adv(3), bxc(2), out(5), jnz(0)
#
# while a != 0:
#   bst(4): B = A % 8
#   bxl(5): B = B ^ 5 aka B ^ 0b101
#   cdv(5): C = A / 2^B aka A >> B
#   bxl(6): B = B ^ 6 aka B ^ 0b110
#   adv(3): A = A / 2^3 aka A >> 3
#   bxc(2): B = B ^ C
#   out(5): output B % 8
#
# Only thing changing A is adv(3)
#
# Substituting backwards:
# outputs:
# B = B ^ C
#   = (B ^ 0b110) ^ C
#   = (B ^ 0b110) ^ (A >> B)
#   = ((B ^ 0b101) ^ 0b110) ^ (A >> (B ^ 0b101))
#   = (((A % 8) ^ 0b101) ^ 0b110) ^ (A >> ((A % 8) ^ 0b101))
#   = (A % 8) ^ 0b11 ^ (A >> ((A % 8) ^ 0b101))
#
#   mod 8 the result
#
# --> B
#   = B ^ C
#   = (B ^ 6) ^ C
#   = (B ^ 6) ^ (A >> B)
#   = (B ^ 5 ^ 6) ^ (A >> (B ^ 5))
#   = (A%8 ^ 5 ^ 6) ^ (A >> (A%8 ^ 5))
#
#


def output(A):
    return (A % 8 ^ 5 ^ 6) ^ (A >> (A % 8 ^ 5))


print(output(1))

# ------------------- #

print("Part 1:", p1)
print("Part 2:", p2)

to_copy = p1 if p2 == 0 else p2
pyperclip.copy(to_copy)
print(f"Copied {'P1' if p2 == 0 else 'P2'}: \"{to_copy}\"")
