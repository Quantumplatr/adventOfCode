import sys
import re
from functools import reduce
import math

input = open(sys.argv[1]).read().strip()

p1 = 0
p2 = 0

# ---- CODE HERE ---- #


# Help from: https://github.com/jonathanpaulson/AdventOfCode/blob/master/2023/12.py
dp = {}

def num_arr2(symbols, groups, index=0, group=0, group_so_far=0):
    key = (index, group, group_so_far)
    if key in dp:
        # print('cache', key)
        return dp[key]
    
    
    # If at end
    if index == len(symbols):
        # If all groups previsouly completed
        if group == len(groups) and group_so_far == 0:
            # print('good')
            return 1
        # Elif groups just finished
        elif group == len(groups) - 1 and groups[group] == group_so_far:
            # print('good')
            return 1
        # Else groups bad
        else:
            # print('bad')
            return 0
        
    # Continue/Recurse
    num = 0
    char = symbols[index]
    for option in [".","#"]:
        # if char == "?":
        #     print('loop', index, option)
        # Do one if option
        # Do both if ?
        if char == option or char == "?":
            if option == ".":
                # If didn't just finish block
                if group_so_far == 0:
                    num += num_arr2(symbols, groups, index+1, group, group_so_far)
                    
                # If did just finish block. If bad block, skip
                elif group < len(groups) and groups[group] == group_so_far:
                    num += num_arr2(symbols, groups, index+1, group+1, 0)
                
            elif option == "#":
                # Continue Group
                num += num_arr2(symbols, groups, index+1, group, group_so_far+1)
                
    # print(symbols, index, group, group_so_far, num)
    dp[key] = num
    return num
    

# Too slow for part 2
# caching didn't really work with symbols and nums and index and group
# refactored into num_arr2 and state space (index, group, group_so_far)
def num_arr1(symbols, nums, index=0, group=-1):
    # if ("".join([str(n) for n in nums]), index, group) in dp:
        # print('cache hit', dp[("".join([str(n) for n in nums]), index, group)], symbols, nums, index, group)
        # return dp[("".join([str(n) for n in nums]), index, group)]

    # Short circuits
    num_hash_left = sum([1 for char in symbols[index:] if char == "#"])
    num_ques_left = sum([1 for char in symbols[index:] if char == "?"])
    num_needed = sum(nums)

    if num_needed > num_hash_left + num_ques_left:
        dp[("".join([str(n) for n in nums]), index, group)] = 0
        return 0
    
    if any([num < 0 for num in nums]):
        return 0

    # print(symbols, nums, index, group)
    if index == len(symbols):
        # print('good e' if all([num == 0 for num in nums]) else 'bad e')

        dp[("".join([str(n) for n in nums]), index, group)] = (
            1 if all([num == 0 for num in nums]) else 0
        )
        return 1 if all([num == 0 for num in nums]) else 0

    char = symbols[index]
    

    if char == ".":
        # Continue
        dp[("".join([str(n) for n in nums]), index, group)] = num_arr1(
            symbols, nums, index + 1, group
        )
        return dp[("".join([str(n) for n in nums]), index, group)]

    elif char == "#":
        # Is fisrt of group
        if index == 0 or symbols[index - 1] == ".":
            group += 1

        # If no more groups or group is used up, return no good arrangements
        if group > 0 and (group == len(nums) or nums[group] <= 0):
            # print('bad #')
            dp[("".join([str(n) for n in nums]), index, group)] = 0
            return 0

        # If room in group
        else:
            # Decrease remaining
            new_nums = list(nums)
            new_nums[group] -= 1

            # Continue
            dp[("".join([str(n) for n in nums]), index, group)] = num_arr1(
                symbols, new_nums, index + 1, group
            )
            return dp[("".join([str(n) for n in nums]), index, group)]

    elif char == "?":
        as_dot = num_arr1(
            symbols[0:index] + "." + symbols[index + 1 :], nums, index + 1, group
        )

        as_hash = 0

        # Is fisrt of group
        if index == 0 or symbols[index - 1] == ".":
            group += 1

        # If no more groups or group is used up, return no good arrangements
        if group > 0 and (group == len(nums) or nums[group] <= 0):
            # print('bad ?')
            dp[("".join([str(n) for n in nums]), index, group)] = as_dot
            return as_dot

        # If room in group
        else:
            # Decrease remaining
            new_nums = list(nums)
            new_nums[group] -= 1

            # Continue
            as_hash = num_arr1(
                symbols[0:index] + "#" + symbols[index + 1 :],
                new_nums,
                index + 1,
                group
            )

        # print('? at', index, ":", as_dot, as_hash)
        return as_dot + as_hash


for i, line in enumerate(input.split("\n")):
    symbols, nums = line.split(" ")
    nums = [int(n) for n in re.findall(r"(\d+)", nums)]

    dp.clear()
    arr = num_arr2(symbols, nums)
    print(symbols, nums, arr)
    

    p1 += arr

print("Part 1:", p1)

for i, line in enumerate(input.split("\n")):
    symbols, nums = line.split(" ")
    nums = [int(n) for n in re.findall(r"(\d+)", nums)]
    
    symbols = "?".join([symbols] * 5)
    nums *= 5

    dp.clear()
    arr = num_arr2(symbols, nums)
    print(symbols, nums, arr)

    p2 += arr

# ------------------- #

print("Part 2:", p2)
