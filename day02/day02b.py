import sys
import functools

# R G B
in_bag = {
    "red": 12,
    "green": 13,
    "blue": 14
}

pow_sum = 0

for line in open(sys.argv[1], "r").readlines():
    line = line.strip()

    game, draws = line.split(":")
    _, game_id = game.split(" ")

    maxs = {
        "red": 0,
        "green": 0,
        "blue": 0
    }

    for draw in draws.split(";"):
        items = draw.strip().split(",")
        for item in items:
            item = item.strip()
            count, color = item.split()
            maxs[color] = max(int(count), maxs[color])

    power = functools.reduce( lambda x, y: x * y, maxs.values())
    print(f"Game {game_id}: Red = {maxs['red']}, Green = {maxs['green']}, Blue = {maxs['blue']} --> {power}")
    
    pow_sum += power

print(pow_sum)