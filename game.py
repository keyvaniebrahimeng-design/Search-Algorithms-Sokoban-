
def load_level(path):

    with open(path, "r") as f:
        raw = [line.rstrip("\n") for line in f.readlines()]

    width = max(len(line) for line in raw)
    level = [line.ljust(width) for line in raw]

    walls = set()
    goals = set()
    boxes = set()
    player = None

    for y, row in enumerate(level):
        for x, ch in enumerate(row):

            if ch == '#':
                walls.add((x, y))

            elif ch == '.':
                goals.add((x, y))

            elif ch == '$':
                boxes.add((x, y))

            elif ch == '@':
                player = (x, y)

            elif ch == '*':
                boxes.add((x, y))
                goals.add((x, y))

            elif ch == '+':
                player = (x, y)
                goals.add((x, y))

    if player is not None and not isinstance(player, tuple):
        player = tuple(player)

    return level, walls, goals, boxes, player


def move_player(player, boxes, move, walls):

    if move == "U":
        dx, dy = (0, -1)

    elif move == "D":
        dx, dy = (0, 1)

    elif move == "L":
        dx, dy = (-1, 0)

    elif move == "R":
        dx, dy = (1, 0)

    else:
        return player, boxes

    new = (player[0] + dx, player[1] + dy)

    if new in walls:
        return player, boxes

    boxes = set(boxes)

 
    if new in boxes:

        new_box = (new[0] + dx, new[1] + dy)

     
        if new_box in walls or new_box in boxes:
            return player, boxes

        boxes.remove(new)
        boxes.add(new_box)

    return tuple(new), boxes


def is_goal(boxes, goals):
    return boxes == goals
