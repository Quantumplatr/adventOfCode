import sys
from functools import reduce

input = open(sys.argv[1]).read().strip()

# input = "abcdefgh" # Expects: abcdffaa
# input = "ghijklmn" # Expects: ghjaabcc

letters = "abcdefghijklmnopqrstuvwxyz"

p1 = 0
p2 = 0

# ---- CODE HERE ---- #


def is_valid_pass(pwd: str) -> bool:
    # --- #1 --- #
    # Must have 3 in a row incr (e.g. abc, xyz)
    found = False
    for i, char in enumerate(pwd):
        # Too far
        if i + 2 == len(pwd):
            break

        char_ind = letters.index(char)

        # pattern = letters[char_ind:] + letters[:char_ind]
        pattern = letters[char_ind:] # Don't wrap this

        if pattern.startswith(pwd[i : i + 3]):
            found = True

    if not found:
        return False

    # --- #2 --- #
    # Can't have 'i', 'o', or 'l':
    if any([char in pwd for char in ("i", "o", "l")]):
        return False

    # --- #3 --- #
    # Must contain two diff non-overlapping pairs
    pairs = set()
    for i, char in enumerate(pwd):
        # Too far
        if i + 1 == len(pwd):
            break

        double = pwd[i : i + 2]

        if double[0] == double[1]:
            pairs.add(double)

    if len(pairs) < 2:
        return False

    return True


def increment(pwd: str) -> str:
    new = ""
    
    # Smart Check for 'iol' (e.g.: incr "hijkl" to "hjaaa")
    if any([char in pwd for char in 'iol']):
        i_ind = pwd.index('i') if 'i' in pwd else len(pwd) + 1
        o_ind = pwd.index('o') if 'o' in pwd else len(pwd) + 1
        l_ind = pwd.index('l') if 'l' in pwd else len(pwd) + 1
        
        min_ind = min([i_ind, o_ind, l_ind])
        
        new_char = 'j' if min_ind == i_ind else 'p' if min_ind == o_ind else 'm'
        new = pwd[:min_ind] + new_char + ("a" * (len(pwd) - (min_ind + 1)))
        return new
    

    should_inc = True
    for i, char in reversed(list(enumerate(pwd))):
        new_char = char

        if should_inc:
            char_ind = letters.index(char)
            new_char = letters[(char_ind + 1) % len(letters)]

            should_inc = False if new_char != "a" else True

        new = new_char + new

    return new


start = input

new = start
while not is_valid_pass(new):
    new = increment(new)
    # print(new)

p1 = new

new = increment(new)
while not is_valid_pass(new):
    new = increment(new)
    # print(new)

p2 = new

# ------------------- #


print(p1, p2)
