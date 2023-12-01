import sys
from functools import reduce

input = open(sys.argv[1]).read().strip()

p1 = 0
p2 = 0

# ---- CODE HERE ---- #

gamma_rate = 0
epsilon_rate = 0

lines = input.split("\n")

one_count = [0] * len(lines[0])
for binary in lines:
    for i, bit in enumerate(binary):
        if bit == "1":
            one_count[i] += 1

for i, count in enumerate(one_count):
    if count > len(lines) / 2:
        gamma_rate = (gamma_rate << 1) + 1
        epsilon_rate = epsilon_rate << 1
    else:
        gamma_rate = gamma_rate << 1
        epsilon_rate = (epsilon_rate << 1) + 1

# print(bin(gamma_rate), bin(epsilon_rate))


# Get oxygen
oxygen_list = lines

digit = 0
while len(oxygen_list) != 1 and digit < len(lines[0]):
    count = 0

    for binary in oxygen_list:
        count += int(binary[digit])

    least_common = 1 if count >= len(oxygen_list) / 2 else 0

    oxygen_list = [
        binary for binary in oxygen_list if int(binary[digit]) == least_common
    ]

    digit += 1

oxygen = int(oxygen_list[0], base=2)

# Get co2
co2_list = lines

digit = 0
while len(co2_list) != 1 and digit < len(lines[0]):
    count = 0

    for binary in co2_list:
        count += int(binary[digit])

    least_common = 1 if count < len(co2_list) / 2 else 0

    if count == len(co2_list):
        least_common = 1
    
    if count == 0:
        least_common = 0

    co2_list = [binary for binary in co2_list if int(binary[digit]) == least_common]

    digit += 1

co2 = int(co2_list[0], base=2)

# print(oxygen, co2)

p1 = gamma_rate * epsilon_rate
p2 = oxygen * co2

# ------------------- #

print(p1, p2)
