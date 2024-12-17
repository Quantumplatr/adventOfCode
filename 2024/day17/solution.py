import enum
import sys
import re
from functools import reduce
import math
import pyperclip

# Solved:
# - P1: 2024-12-16
# - P2: 2024-12-17
#
# P1 Thoughts:
# - I'm pretty happy w/ my P1
# - Not too difficult of a program
# - Made a few tiny mistakes lot using OR instead of XOR
# - Worked pretty immediately tho
#
# P2 Thoughts:
# - I started with brute force to just have it running
# - Then I started trying to cache program states to outputs
#   so I could skip running the program if it knew the output.
#   This sped it up but not nearly enough.
# - At this point I looked for hints on the subreddit. Found that
#   a few people did brute force but smarter where they jumped closer
#   to the result by doubling A until it had the right number of digits.
#   I tried to be smarter about that but it still wasn't working.
# - Then I saw that some people reverse engineered the program to find
#   how to calculate the answer instead of search for it. This is what
#   I started doing.
# - I think if it wasn't super late and I wasn't tired, I would've gotten
#   to this faster. I knew there was going to be some pattern to recognize
#   as there was a lot of mod 8s. I just didn't see it before I looked
#   for hints. If I had went straight to reverse engineering instead of
#   trying caching I might've finished it before I got too tired last night
#   and gave up. It also appears you don't need a full reverse engineered
#   program as long as you notice that it handles A in 3 bit chunks.
# - Long story short, caching isn't always the answer. I should notice
#   if the input I have is short b/c then it might be worth actually manually
#   looking at the input to see if there's a pattern to recognize. If I think
#   there might be a pattern, I should try to look for it before trying
#   everything else.
# - Still pretty happy with my result as I understand it pretty well now.
#   I'll do better next time now that I have some more advent of code strats

input = open(sys.argv[1]).read().strip()

p1 = 0
p2 = 0

# ---- CODE HERE ---- #


registers, program = input.split("\n\n")

a, b, c = [int(n) for n in re.findall(r"(\d+)", registers)]

operations = [int(n) for n in re.findall(r"(\d+)", program)]

pointer = 0


# Gets the combo value for a given input
# 0-3 are literal
# 4-6 are A, B, or C registers
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


# Op code 0
# Uses combo input to shift A
# A = A >> value aka A / 2^value
def adv(input):
    global a
    value = get_combo(input)
    a = a >> value
    return None


# Op code 1
# Uses literal input
# B = B XOR input
def bxl(input):
    global b
    b = b ^ input
    return None


# Op code 2
# Uses combo input
# B = value % 8
def bst(input):
    global b
    value = get_combo(input) % 8
    b = value
    return None


# Op code 3
# If A is not 0, jump to input
# Updates `pointer`
def jnz(input):
    global a
    global pointer
    if a == 0:
        return None
    else:
        pointer = input
        return None


# Op code 4
# Does not use input
# B = B XOR C
def bxc(input):
    global b
    global c
    b = b ^ c
    return None


# Op code 5
# Uses combo input
# Returns value % 8
def out(input):
    return get_combo(input) % 8


# Op code 6
# Uses combo input
# B = A >> value aka A / 2^value
def bdv(input):
    global b
    value = get_combo(input)
    b = a >> value
    return None


# Op code 7
# Uses combo input
# C = A >> value aka A / 2^value
def cdv(input):
    global c
    value = get_combo(input)
    c = a >> value
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


def run(operations):
    global pointer
    global a
    global b
    global c
    output = []
    pointer = 0
    while pointer < len(operations):
        op = operations[pointer]
        input = operations[pointer + 1]

        res = ops[op](input)
        if res is not None:
            output.append(res)

        # Jump conditions
        if op == 3 and a != 0:
            continue

        pointer += 2

    return output


p1 = ",".join([str(n) for n in run(operations)])


# --- Reverse engineering the program --- #
#
# Program: 2,4,1,5,7,5,1,6,0,3,4,2,5,5,3,0
#
# Resulting operations: bst(4), bxl(5), cdv(5), bxl(6), adv(3), bxc(2), out(5), jnz(0)
#
# Pseudocode
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
# Each iteration we get some value based on A % 8 and then we shift A by 3
#
# Substituting backwards:
# --> B                                 % 8
#   = B ^ C                             % 8
#   = (B ^ 6) ^ C                       % 8
#   = (B ^ 6) ^ (A >> B)                % 8
#   = (B ^ 5 ^ 6) ^ (A >> (B ^ 5))      % 8
#   = (A%8 ^ 5 ^ 6) ^ (A >> (A%8 ^ 5))  % 8
#   = (A%8 ^ 3) ^ (A >> (A%8 ^ 5))      % 8
#
# This means that every 3 binary digits of the original A value correlate to one output digit (0-7)
# Instead of brute forcing every A value, we just check which 3 binary digits make the output correct
#
# For example:
# If A is 3 aka 0b101, the output is 0.
# If A is 3*8 + 2 aka 0b101_000, the output is 3,0.
# - The rightmost 000 gives 3 and then the 101 gives 0.
# A as 0b101_000_000 would give 5,3,0.
#
# Notice that 5,3,0 matches the end of the program.
#
# Multiple values can result in the same output, but we only need one.
# So we just check that if it breaks down the road, we would've needed a different
# 3 digits of binary.
#
# Handling 3 digits of binary is basically base 8 conversion.


# Turn base 8 digits into base 10
def base_change(digits):
    o = 0
    for i, d in enumerate(digits):
        o += d * pow(8, i)

    return o


# Condensed program running.
# This outputs only the next output from a full program run on
# registers (A,B,C) = (A parameter,0,0)
# This only works for my advent of code input
def next_out(A):
    return (((A % 8) ^ 3) ^ (A >> ((A % 8) ^ 5))) % 8


# Recursive function to find the correct base 8 digits
# One base 8 digit maps to 1 output digit
def find(digits):
    global a
    global b
    global c
    global pointer

    # End condition
    if len(digits) == len(operations):
        return digits

    # Full value so far
    so_far = base_change(digits)

    # Digit index
    digit = len(operations) - 1 - len(digits)

    # Output desired
    correct = operations[digit]

    # Potential digits to get output
    potential = []
    for i in range(8):
        # Could run a program on potential a,0,0 values,
        # or we can use our shortcut `next_out` that I
        # reverse engineered from the program

        # Get output from using i as the next digit
        # We shift the value so far and add the new digit
        # E.g. 0b101_000 -> 0b101_000_001 for i == 0b001
        val = next_out(so_far * 8 + i)

        # If the output is correct, this digit is a potential
        if val == correct:
            potential.append(i)

    # If no potential digits match, this path is invalid
    if len(potential) == 0:
        return None

    # For each potential digit, recursively continue the search
    for p in potential:
        # Add digit at front
        new_digits = [p] + digits

        # Search
        result = find(new_digits)

        # If result found, we did it!
        if result is not None:
            return result

    # This will happen when there are potential digits but none work
    return None


# Find digits that match output
# Start with [] as we don't know any digits
digits = find([])

# P2 is base 8 digits in base 10
p2 = base_change(digits)

# # Can confirm that p2 is correct by running the program
# # and confirming that it outputs the correct values
# print("want", operations)
# a = p2
# b = 0
# c = 0
# print("res", run(operations))
# print(p2)

# ------------------- #

print("Part 1:", p1)
print("Part 2:", p2)

to_copy = p1 if p2 == 0 else p2
pyperclip.copy(to_copy)
print(f"Copied {'P1' if p2 == 0 else 'P2'}: \"{to_copy}\"")
