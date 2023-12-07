import sys
import re
from functools import reduce, cmp_to_key

input = open(sys.argv[1]).read().strip()

p1 = 0
p2 = 0

# ---- CODE HERE ---- #

def get_hand_value2(counts):
    just_counts = [c for _, c in counts.items()]
    just_counts_no_jokers = [c for card, c in counts.items() if card != "J"]
    joker_count = 0 if "J" not in counts else counts["J"]

    val = 0
    
    # 5oak
    if 5 in just_counts or (5 - joker_count) in just_counts_no_jokers or joker_count == 5:
        val = 6
        
    # 4oak
    elif 4 in just_counts or (4 - joker_count) in just_counts_no_jokers or joker_count == 4:
        val = 5
        
    # full house & 3oak
    elif 3 in just_counts or (3 - joker_count) in just_counts_no_jokers or joker_count == 3:
        if 3 in just_counts:
            if 2 in just_counts or (2 - joker_count) in just_counts_no_jokers:
                val = 4  # full house w/ 3oak w/o joker
            else:
                val = 3  # 3oak
        else:  # jokers if any for 3oak
            # full 3oak of jokers
            if joker_count == 3:
                if 2 in just_counts_no_jokers:
                    val = 4  # full house w/ 3oak all jokers
                else:
                    val = 3

            # if 2 jokers, only need a pair
            elif joker_count == 2:
                if 2 in just_counts_no_jokers:
                    val = 4  # full house w/ 2 jokers in 3oak
                else:
                    val = 3

            # if 1 joker, need 2 pair
            elif joker_count == 1:
                if len([c for c in just_counts_no_jokers if c == 2]) == 2:
                    val = 4  # full house w/ one joker and 2 pair
                else:
                    val = 3

            # 3oak
            else:
                val = 3

    # pairs
    elif 2 in just_counts or joker_count > 0:
        if 2 in just_counts and joker_count > 0:
            val = 2  # 2 pair w/ joker
        elif len([c for c in just_counts if c == 2]) == 2:
            val = 2  # 2 pair w/o joker
        else:
            val = 1  # one pair
            
    return val


def compare_hands2(g1, g2):
    h1, b1 = g1
    h2, b2 = g2

    h1_counts = {}

    h2_counts = {}

    for card in h1:
        if card in h1_counts:
            h1_counts[card] += 1
        else:
            h1_counts[card] = 1

    for card in h2:
        if card in h2_counts:
            h2_counts[card] += 1
        else:
            h2_counts[card] = 1

    r1 = get_hand_value2(h1_counts)
    r2 = get_hand_value2(h2_counts)

    if r1 == r2:
        for i, card1 in enumerate(h1):
            card2 = h2[i]

            if card1 == card2:
                continue

            CARD_VALUES = [
                "J",
                "2",
                "3",
                "4",
                "5",
                "6",
                "7",
                "8",
                "9",
                "T",
                "Q",
                "K",
                "A",
            ]

            i1 = CARD_VALUES.index(card1)
            i2 = CARD_VALUES.index(card2)

            return 1 if i1 > i2 else -1

    if r1 == r2:
        return 0

    return 1 if r1 > r2 else -1


def compare_hands1(g1, g2):
    h1, b1 = g1
    h2, b2 = g2

    h1_counts = {}

    h2_counts = {}

    for card in h1:
        if card in h1_counts:
            h1_counts[card] += 1
        else:
            h1_counts[card] = 1

    for card in h2:
        if card in h2_counts:
            h2_counts[card] += 1
        else:
            h2_counts[card] = 1

    h1_c = [c for _, c in h1_counts.items()]
    h2_c = [c for _, c in h2_counts.items()]

    r1 = 0
    if 5 in h1_c:
        r1 = 6
    elif 4 in h1_c:
        r1 = 5
    elif 3 in h1_c and 2 in h1_c:
        r1 = 4
    elif 3 in h1_c:
        r1 = 3
    elif 2 in h1_c:
        if len([c for c in h1_c if c == 2]) == 2:
            r1 = 2
        else:
            r1 = 1

    r2 = 0
    if 5 in h2_c:
        r2 = 6
    elif 4 in h2_c:
        r2 = 5
    elif 3 in h2_c and 2 in h2_c:
        r2 = 4
    elif 3 in h2_c:
        r2 = 3
    elif 2 in h2_c:
        if len([c for c in h2_c if c == 2]) == 2:
            r2 = 2
        else:
            r2 = 1

    if r1 == r2:
        for i, card1 in enumerate(h1):
            card2 = h2[i]

            if card1 == card2:
                continue

            CARD_VALUES = [
                "2",
                "3",
                "4",
                "5",
                "6",
                "7",
                "8",
                "9",
                "T",
                "J",
                "Q",
                "K",
                "A",
            ]

            i1 = CARD_VALUES.index(card1)
            i2 = CARD_VALUES.index(card2)

            return 1 if i1 > i2 else -1

    if r1 == r2:
        return 0

    return 1 if r1 > r2 else -1


hands = []
for line in input.split("\n"):
    hand, bid = line.split(" ")

    bid = int(bid)

    counts = {}
    for card in hand:
        if card in counts:
            counts[card] += 1
        else:
            counts[card] = 0

    hands.append((hand, bid))

hands.sort(key=cmp_to_key(compare_hands1))

p1 = sum([b * (i + 1) for i, (h, b) in enumerate(hands)])

hands.sort(key=cmp_to_key(compare_hands2))

p2 = sum([b * (i + 1) for i, (h, b) in enumerate(hands)])

to_write = "\n".join([str(h) for h in hands])

f = open("output.txt", "w")
f.write(to_write)
f.close()


# ------------------- #

print(p1, p2)
