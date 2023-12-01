import sys
from functools import reduce

input = open(sys.argv[1]).read().strip()

p1 = 0
p2 = 0

# ---- CODE HERE ---- #

nice_count1 = 0
nice_count2 = 0

for line in input.split("\n"):
    
    
    # --- p1 --- #
    is_nice1 = True
    
    # Bad patterns
    if any(pattern in line for pattern in ('ab', 'cd', 'pq', 'xy')):
        is_nice1 = False
    
    last_char = ""
    vowel_count = 0
    has_double = False
    for char in line:
        
        # Double letter
        if char == last_char:
            has_double = True
            
        # Vowel check
        if char in ('a','e','i','o','u'):
            vowel_count += 1
        
        last_char = char
        
    # Enough vowels and has double
    if vowel_count < 3 or not has_double:
        is_nice1 = False
        
    # Check if nice
    if is_nice1:
        nice_count1 += 1
        
    # --- p2 --- #
    
    found_double_pair = False
    found_repeat_after1 = False
    
    for i, char in enumerate(line):
        
        # Pairs
        if line[i:i+2] in line[i+2:]:
            found_double_pair = True
                
        # Repeat after 1
        if i < len(line)-2 and char == line[i+2]:
            found_repeat_after1 = True
                    
        
    if found_repeat_after1 and found_double_pair:
        nice_count2 += 1
        
p1 = nice_count1
p2 = nice_count2

# ------------------- #

print(p1, p2)