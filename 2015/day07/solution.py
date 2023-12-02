import sys
from functools import reduce

input = open(sys.argv[1]).read().strip()

p1 = 0
p2 = 0

# ---- CODE HERE ---- #


def bit_not(v: str) -> str:
    full_v = "0" * (16 - len(v)) + v
    return "".join(["0" if bit == "1" else "1" for bit in full_v])


def bit_and(v1: str, v2: str) -> str:
    v = ""

    full_v1 = "0" * (16 - len(v1)) + v1
    full_v2 = "0" * (16 - len(v2)) + v2

    for i, bit1 in enumerate(full_v1):
        bit2 = full_v2[i]
        v += "1" if bit1 == "1" and bit2 == "1" else "0"

    return v


def bit_or(v1: str, v2: str) -> str:
    v = ""

    full_v1 = "0" * (16 - len(v1)) + v1
    full_v2 = "0" * (16 - len(v2)) + v2

    for i, bit1 in enumerate(full_v1):
        bit2 = full_v2[i]
        v += "1" if bit1 == "1" or bit2 == "1" else "0"

    return v


def bit_lshift(v1: str, v2: str) -> str:
    v = ""
    full_v1 = "0" * (16 - len(v1)) + v1

    shift_by = int(v2, base=2)

    for i, bit1 in enumerate(full_v1):
        v += full_v1[i + shift_by] if i + shift_by < len(full_v1) else "0"

    return v


def bit_rshift(v1: str, v2: str) -> str:
    v = ""

    shift_by = int(v2, base=2)

    for i, bit1 in enumerate(v1):
        v += v1[i - shift_by] if i - shift_by >= 0 else "0"

    return v


wires = {}

instructions = input.split("\n")

# Repeat until all instructions complete
while len(instructions) > 0:
    completed_instructions = []

    # Attempt all instructions
    for i, instr in enumerate(instructions):
        value, into = instr.split(" -> ")

        tokens = value.split(" ")

        # Value
        if len(tokens) == 1:
            v = value
            if not v.isnumeric():
                if v not in wires:
                    continue
                v = wires[v]
            else:
                v = bin(int(value))[2:]

            wires[into] = v

        # Not
        elif len(tokens) == 2:
            _, v = tokens

            if not v.isnumeric():
                if v not in wires:
                    continue
                v = wires[v]
            else:
                v = bin(int(v))[2:]

            wires[into] = bit_not(v)

        # Other
        else:
            v1, oper, v2 = tokens

            if not v1.isnumeric():
                if v1 not in wires:
                    continue
                v1 = wires[v1]
            else:
                v1 = bin(int(v1))[2:]

            if not v2.isnumeric():
                if v2 not in wires:
                    continue
                v2 = wires[v2]
            else:
                v2 = bin(int(v2))[2:]

            match oper:
                case "AND":
                    wires[into] = bit_and(v1, v2)
                case "OR":
                    wires[into] = bit_or(v1, v2)
                case "LSHIFT":
                    wires[into] = bit_lshift(v1, v2)
                case "RSHIFT":
                    wires[into] = bit_rshift(v1, v2)

        completed_instructions.append(i)

    # Remove completed
    for i in range(len(completed_instructions) - 1, -1, -1):
        del instructions[completed_instructions[i]]


decimal_wires = {}

for key, value in wires.items():
    decimal_wires[key] = int(value, base=2)


p1 = decimal_wires["a"] if "a" in decimal_wires else -1

# --- P2 --- #

wires = {}
wires["b"] = bin(p1)[2:]

instructions = input.split("\n")

# Repeat until all instructions complete
while len(instructions) > 0:
    completed_instructions = []

    # Attempt all instructions
    for i, instr in enumerate(instructions):
        value, into = instr.split(" -> ")
        
        # Skip b for part 2
        if into == "b":
            completed_instructions.append(i)
            continue

        tokens = value.split(" ")

        # Value
        if len(tokens) == 1:
            v = value
            if not v.isnumeric():
                if v not in wires:
                    continue
                v = wires[v]
            else:
                v = bin(int(value))[2:]

            wires[into] = v

        # Not
        elif len(tokens) == 2:
            _, v = tokens

            if not v.isnumeric():
                if v not in wires:
                    continue
                v = wires[v]
            else:
                v = bin(int(v))[2:]

            wires[into] = bit_not(v)

        # Other
        else:
            v1, oper, v2 = tokens

            if not v1.isnumeric():
                if v1 not in wires:
                    continue
                v1 = wires[v1]
            else:
                v1 = bin(int(v1))[2:]

            if not v2.isnumeric():
                if v2 not in wires:
                    continue
                v2 = wires[v2]
            else:
                v2 = bin(int(v2))[2:]

            match oper:
                case "AND":
                    wires[into] = bit_and(v1, v2)
                case "OR":
                    wires[into] = bit_or(v1, v2)
                case "LSHIFT":
                    wires[into] = bit_lshift(v1, v2)
                case "RSHIFT":
                    wires[into] = bit_rshift(v1, v2)

        completed_instructions.append(i)

    # Remove completed
    for i in range(len(completed_instructions) - 1, -1, -1):
        del instructions[completed_instructions[i]]


decimal_wires = {}

for key, value in wires.items():
    decimal_wires[key] = int(value, base=2)


p2 = decimal_wires["a"] if "a" in decimal_wires else -1

# ------------------- #

print(p1, p2)
