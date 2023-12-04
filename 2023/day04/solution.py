import sys
import re
from functools import reduce

input = open(sys.argv[1]).read().strip()

p1 = 0
p2 = 0

# ---- CODE HERE ---- #

total = 0

cards = {}

for i, line in enumerate(input.split("\n"), 1):
    # Initial Strat
    # card, num_str = line.split(": ")
    # nums1, nums2 = num_str.split("|")

    # first_nums = [int(n) for n in re.findall(r"\d+", nums1)]
    # second_nums = [int(n) for n in re.findall("\d+", nums2)]

    # Regex Strat after lots of regex learning
    # Idea is:
    #   first:  (numbers)(not before ":")(before "|")
    #   second: (numbers)(not before ":")(not before "|")
    first_nums = [int(n) for n in re.findall(r"(\d+)(?!:)(?=.*\|)", line)]
    second_nums = [int(n) for n in re.findall(r"(\d+)(?!:)(?!.*\|)", line)]

    print(first_nums, second_nums)

    cards[i] = {"a": first_nums, "b": second_nums}

    win_count = 0
    for num in second_nums:
        if num in first_nums:
            win_count += 1

    if win_count > 0:
        total += 2 ** (win_count - 1)


p1 = total

# print(cards)

count = 0
queue = dict(zip(cards.keys(), [1] * len(cards.keys())))
while len(queue) > 0:
    card = min(queue.keys())

    a = cards[card]["a"]
    b = cards[card]["b"]

    matching = 0
    for num in b:
        if num in a:
            matching += 1

    # print(matching, queue)

    for n in range(matching):
        val = n + card + 1
        queue[val] += queue[card]

    count += queue[card]

    del queue[card]

p2 = count


# ------------------- #

print(p1, p2)
