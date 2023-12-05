import sys
import re
from functools import reduce

input = open(sys.argv[1]).read().strip()

p1 = 0
p2 = 0

# ---- CODE HERE ---- #


def range_inter(r1, r2):
    s1, e1 = r1
    s2, e2 = r2
    
    if e1 < s2 or e2 < s1:
        return None

    return (max([s1, s2]), min([e1, e2]))


seeds = []

maps = {}
mappings = {}

# PARSE INPUT INTO MAPPINGS
for ind, map in enumerate(input.split("\n\n")):
    # print("parsing", ind, "/", len(input.split("\n\n")))

    if map.startswith("seeds:"):
        seeds = [int(seed) for seed in re.findall(r"(\d+)", map)]
        continue

    from_key, to_key = re.findall(r"(\w+)-to-(\w+)", map.split("\n")[0])[0]

    values = [
        [int(v) for v in re.findall(r"(\d+)", line)] for line in map.split("\n")[1:]
    ]

    maps[from_key] = to_key
    mappings[from_key] = {}

    for index, group in enumerate(values):
        # print("\tgroup",index,"/",len(values))

        dest, source, length = group

        mappings[from_key][(source, source + length - 1)] = (dest, dest + length - 1)


# print(mappings)

# GO THROUGH SEEDS AND ITERATE OVER MAPS
# UNTIL AT LAST MAP
locs1 = []
for i, seed in enumerate(seeds):
    # print(i, "/", len(seeds))

    # print()

    curr_map = "seed"
    curr_val = seed

    while curr_map in maps:
        # print(curr_map, curr_val)

        # Check if curr_val in mappings[from_key]
        for source_start_end, dest_start_end in mappings[curr_map].items():
            if source_start_end[0] <= curr_val <= source_start_end[1]:
                # print(mappings[curr])
                # print(source_range, dest_range, dest_range[0] + (curr_val - source_range[0]))
                curr_val = dest_start_end[0] + (curr_val - source_start_end[0])
                break

        curr_map = maps[curr_map]

        if curr_map == "location":
            locs1.append(curr_val)
            
p1 = min(locs1)


# --- p2 --- #

# Treat nums as pairs
seed_pairs = [
    (int(s1), int(s2))
    for s1, s2 in re.findall(r"(\d+) (\d+)", " ".join([str(s) for s in seeds]))
]

# Turn pairs into ranges
seed_ranges = [(start, start + length - 1) for start, length in seed_pairs]

locs2 = []

def get_min_loc_in_range(start, end, at_map):
    
    # Base case. Want minimum value of last mapping
    if at_map not in maps:
        return start

    # Make queue of ranges. Recurse into each range at the end    
    queue = [(start,end)]
    
    # Resulting ranges based on mapping 
    dests = []
    
    # Sources is mostly for debugging. Indexes match dests array to see
    # what the mapping changed
    sources = []
    
    # Go over all ranges
    # Ranges can split based on intersection with mapping
    while len(queue) != 0:
        
        # _c for current 
        # s for start
        # e for end
        
        # Pop from queue
        s_c, e_c = queue[0]
        queue = queue[1:]
        
        
        had_overlap = False
        for source_r, dest_r in mappings[at_map].items():
            
            # Get mapping and shift that would entail
            s_source, e_source = source_r
            shift = dest_r[0] - s_source
            
            # Get overlap with current range
            inter = range_inter(source_r, (s_c, e_c))
            
            # If no overlap, no mapping to do
            if inter is None:
                continue
            had_overlap = True
            
            s_i, e_i = inter
            
            # split into 3 sections: [  1 (  inter  ]  2  )
            
            # Lower split
            s1 = min([s_source,s_c])
            e1 = max([s_source-1,s_c-1]) # exclusive
            
            # Upper split
            s2 = min([e_source+1, e_c+1]) # exclusive
            e2 = max([e_source, e_c])
            
            # Finish mapping intersecting range
            dests.append((s_i + shift,e_i + shift))
            sources.append((s_i, e_i))
            
            # If lower split is in current range, add to queue for it to be checked
            if range_inter((start,end), (s1,e1)) is not None:
                queue.append((s1,e1))
                
            # If upper split is in current range, add to queue for it to be checked
            if range_inter((start,end), (s2,e2)) is not None:
                queue.append((s2,e2))
            
            break
            
        
        # If no overlap to any mapping, mapping is just 1-1
        if not had_overlap:
            dests.append((s_c, e_c))
            sources.append((s_c, e_c))
            
    # Once here, dests contains ranges of all mappings
    # Go through all of these split ranges recursively
    # Want minimal location value        
    return min([get_min_loc_in_range(s,e,maps[at_map]) for s,e in dests])
    
    
# Get minimum location from all starting ranges
p2 = min([get_min_loc_in_range(start,end, "seed") for start,end in seed_ranges])

# ------------------- #

print(p1, p2)
