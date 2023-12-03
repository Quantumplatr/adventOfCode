import sys
from functools import reduce

input = open(sys.argv[1]).read().strip()

p1 = 0
p2 = 0

# ---- CODE HERE ---- #

cookies = {}

for line in input.split("\n"):
    cookie, info = line.split(": ")

    cookies[cookie] = {}

    info = info.split(", ")

    for stat in info:
        tokens = stat.split(" ")
        cookies[cookie][tokens[0]] = int(tokens[1])

# --- Linear Programming Problem --- #

# Constraints:
# - sum m_i = 100 where m_i is the measurement for the ith cookie
# - 0 <= m_i <= 100 for all m_i

# Objective Function:
# - maximize prod_j sum_i m_i*x_ij

# --- INSTEAD WE BRUTE FOOOORCE --- #

cookie_list = list(cookies.keys())


def recur(cookie_ind: int, m_left: int, m_vals: [int], cal_must_be=None) -> int:

    # Loop over possible usages
    if cookie_ind != len(cookie_list) - 1:
        max_so_far = -1
        for i in range(0, m_left):

            new_m_vals = list(m_vals)
            new_m_vals[cookie_ind] = i

            result = recur(cookie_ind + 1, m_left - i, new_m_vals, cal_must_be)
            
            max_so_far = max([max_so_far, result])
        return max_so_far
    else:
        new_m_vals = list(m_vals)
        new_m_vals[cookie_ind] = m_left  # Use what's left as it's last cookie

        cap = 0
        dur = 0
        flav = 0
        tex = 0
        cal = 0

        for i, cookie in enumerate(cookie_list):
            cap += new_m_vals[i] * cookies[cookie]["capacity"]
            dur += new_m_vals[i] * cookies[cookie]["durability"]
            flav += new_m_vals[i] * cookies[cookie]["flavor"]
            tex += new_m_vals[i] * cookies[cookie]["texture"]
            cal += new_m_vals[i] * cookies[cookie]["calories"]
            
        cap = max([0, cap])
        dur = max([0, dur])
        flav = max([0, flav])
        tex = max([0, tex])
        
        if cal_must_be is not None:
            if cal != cal_must_be:
                return -1

        return cap * dur * flav * tex

p1 = recur(0, 100, [0] * len(cookie_list))
p2 = recur(0, 100, [0] * len(cookie_list), cal_must_be=500)

# ------------------- #

print(p1, p2)
