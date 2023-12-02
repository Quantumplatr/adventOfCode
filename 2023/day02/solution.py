import sys
from functools import reduce

input = open(sys.argv[1]).read().strip()

p1 = 0
p2 = 0

# ---- CODE HERE ---- #

valid_games = []
total = 0

for game_str in input.split("\n"):
    game, data = game_str.split(": ")
    game_num = int(game.split(" ")[1])
    
    min_colors = {
        "blue": None,
        "red": None,
        "green": None
    }
    
    valid = True
    for handful in data.split("; "):
        colors = handful.split(", ")
        
        for color_and_count in colors:
            amount, color = color_and_count.split(" ")
            amount = int(amount)
            
            if color == "red" and amount > 12:
                valid = False
            if color == "green" and amount > 13:
                valid = False
            if color == "blue" and amount > 14:
                valid = False
                
            if min_colors[color] is None:
                min_colors[color] = amount
            else:
                min_colors[color] = max([amount, min_colors[color]])
            
    if valid:
        valid_games.append(game_num)
        
    total += min_colors["blue"] * min_colors["green"] * min_colors["red"]
        
        
p1 = sum(valid_games)
p2 = total

# ------------------- #

print(p1, p2)