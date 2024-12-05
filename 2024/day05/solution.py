import sys
import re
import pyperclip

# Solved: 2024-12-04
# Things I Could've Done Better:
# - I'm pretty proud of how I did especially since I've been sick today (sore throat and foggy)
# - I might've been able to do a few things a bit more concisely
# - Maybe could've parsed better? I think I did pretty well with that tho idk
# - Could've solved the problem a bit faster. Forgot to check that things before current page
#   followed the rules. Remembering that would've saved me a few minutes.

input = open(sys.argv[1]).read().strip()

p1 = 0
p2 = 0

# ---- CODE HERE ---- #

sections = input.split("\n\n")

# - Parse input - #
# Get pairs of rules (e.g. "<before>|<after>")
pairs = [
    (int(group[0]), int(group[1])) for group in re.findall(r"(\d+)\|(\d+)", sections[0])
]

# Convert to dictionary of rules (e.g. {<before>: [<after>, ...]})
pairs_dict = {}
for pair in pairs:
    k, v = pair  # Get key value pair
    if k not in pairs_dict:  # If key doesn't exist, create it
        pairs_dict[k] = []
    pairs_dict[k].append(v)  # Append value to key's array

# Get updates (e.g. "1,2,3,4,5")
updates = [
    # For each row, get all numbers and parse them as integers
    [int(n) for n in re.findall(r"(\d+)", row)]
    for row in sections[1].split("\n")
]


# Check if update is safe
def is_safe(update) -> bool:
    for index, page in enumerate(update):
        # Check that a rule exists
        if page in pairs_dict:
            # Check that nothing that is supposed to be after is before
            if index > 0:
                for pp in update[:index]:
                    if pp in pairs_dict[page]:
                        return False
            # Check that everything after is supposed to be after or doesn't
            # have a rule
            for np in update[index + 1 :]:
                if np not in pairs_dict[page]:
                    return False
    return True


# Return new, fixed update that is safe
def fix(update):
    # Build new update with first element
    # (assume it's safe and fix the rest)
    new_update = [update[0]]

    # For each value we need to use, find a spot where it's safe
    for u in update:
        # Check each position and see if it's safe
        for i in range(len(new_update) + 1):
            # E.g. [1, 2, 3] -> [1, 4, 2, 3]
            # Splice in the new value and check if it's safe
            # NOTE: potentially could've coded this quicker with .insert on a clone
            potential_update = new_update[:i] + [u] + new_update[i:]
            if is_safe(potential_update):
                new_update = potential_update
                break

    return new_update


# Go through each update
for update in updates:
    # P1: Sum of middles of safe updates
    if is_safe(update):
        p1 += update[int(len(update) / 2)]
    # P2: Sum of middles of safe updates with fixed order
    else:
        p2 += fix(update)[int(len(update) / 2)]


# ------------------- #

print("Part 1:", p1)
print("Part 2:", p2)

to_copy = p1 if p2 == 0 else p2
pyperclip.copy(to_copy)
print(f"Copied {'P1' if p2 == 0 else 'P2'}: \"{to_copy}\"")
