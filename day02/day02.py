import sys

# R G B
in_bag = {
    "red": 12,
    "green": 13,
    "blue": 14
}

id_sum = 0

for line in open(sys.argv[1], "r").readlines():
    line = line.strip()

    game, draws = line.split(":")
    _, game_id = game.split(" ")

    game_ok = True
    for draw in draws.split(";"):
        items = draw.strip().split(",")
        for item in items:
            item = item.strip()
            count, color = item.split()
            if int(count) > in_bag[color]:
                print(f"TOO MANY in game {game_id}: {count} {color}")
                game_ok = False
    if game_ok:
        print(f"Game {game_id} is OK")
        id_sum += int(game_id)

print(f"Sum of valid game IDs: {id_sum}")