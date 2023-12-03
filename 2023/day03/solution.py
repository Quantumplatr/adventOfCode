import sys
import re
from functools import reduce

input = open(sys.argv[1]).read().strip()

p1 = 0
p2 = 0

# ---- CODE HERE ---- #

symbols = "!@#$%^&*()-=_/\\[]{}+;:,<>?'\"" # This was dumb lmao. Should've just checked if not num or '.'

part_nums = []

gears = {}

lines = input.split("\n")


def note_gear(row, col, num):
    pos = f"{row},{col}"
    if pos not in gears:
        gears[pos] = []

    gears[pos].append(num)


for row, line in enumerate(lines):
    i = 0
    while i < len(line):
        char = line[i]
        
        # Found num
        if char.isdigit():
            num = int(re.match("\d+", line[i:]).group(0))

            prev_col = max([0, i - 1])
            next_col = min([i + len(str(num)) + 1, len(line) - 1])
            is_part_num = False

            # Check if symbol adjacent
            
            # check prev row
            if row >= 1:
                prev_row = lines[row - 1][prev_col:next_col]

                if any([char in prev_row for char in symbols]):
                    if "*" in prev_row:
                        note_gear(row - 1, prev_row.index("*") + prev_col, num)
                    is_part_num = True

            # Check next row
            if row < len(lines) - 1:
                next_row = lines[row + 1][prev_col:next_col]
                if any([char in next_row for char in symbols]):
                    if "*" in next_row:
                        note_gear(row + 1, next_row.index("*") + prev_col, num)

                    is_part_num = True

            # Check prev char
            if i >= 1 and line[i - 1] in symbols:
                if line[i - 1] == "*":
                    note_gear(row, i - 1, num)
                is_part_num = True

            # Check next char
            if i + len(str(num)) < len(line) - 1 and line[i + len(str(num))] in symbols:
                if line[i + len(str(num))] == "*":
                    note_gear(row, i + len(str(num)), num)
                is_part_num = True

            # Add to list
            if is_part_num:
                part_nums.append(num)

            # Move along
            i += len(str(num))
            continue

        i += 1

p1 = sum(part_nums)

# Get sum of gear ratios
total = 0
for pos, nums in gears.items():    
    if len(nums) == 2:
        ratio = nums[0] * nums[1]
        total += ratio
        
p2 = total

# ------------------- #

print(p1, p2)
