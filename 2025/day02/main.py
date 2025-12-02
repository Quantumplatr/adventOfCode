import sys
import re
from functools import reduce
import math

input = open(sys.argv[1]).read().strip()

p1 = 0
p2 = 0

invalid_ids = []
invalid_ids2 = []

# NOTE: this probably could be optimized but it works


# Reports whether the given string is a repeated string
def does_repeat(id_str: str) -> bool:
    # id_str == 123123123
    full_length = len(id_str)  # e.g. 9

    # Check all possible lengths of repeats
    # E.g.
    # - Length 1 means "11"
    # - Length 2 means "1212"
    # - Length 3 means "123123"
    for length in range(1, full_length):
        # If not clean split, skip
        if full_length % length != 0:
            continue

        # Check against first chunk
        check = id_str[:length]  # e.g. 123123123 -> 123

        # Based of chunk size, check if all chunks match
        repeats = True
        for chunk_ind in range(1, int(full_length / length)):
            check_against = id_str[chunk_ind * length : (chunk_ind + 1) * length]
            if check != check_against:
                repeats = False
                break
        if repeats:
            return True

    return False


lines = input.split(",")
for line in lines:
    start, end = re.findall(r"(\d+)-(\d+)", line)[0]
    for id in range(int(start), int(end) + 1):
        id_str = str(id)
        l = len(id_str)

        # Check first and second halves
        if l % 2 == 0:
            if id_str[: int(l / 2)] == id_str[int(l / 2) :]:
                invalid_ids.append(id)

        # Check arbitrary repeats
        if does_repeat(id_str):
            invalid_ids2.append(id)

p1 = sum(invalid_ids)
p2 = sum(invalid_ids2)

print("Part 1:", p1)
print("Part 2:", p2)
