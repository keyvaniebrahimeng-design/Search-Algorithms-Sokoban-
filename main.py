

import pygame
import time
import os

from game import *
from solver import *
from graphics import TILE, PANEL, Button, draw_game

pygame.init()



BASE_DIR = os.path.dirname(os.path.abspath(__file__))

levels = [
    os.path.join(BASE_DIR, "levels", "level1.txt"),
    os.path.join(BASE_DIR, "levels", "level2.txt"),
    os.path.join(BASE_DIR, "levels", "level3.txt"),
    os.path.join(BASE_DIR, "levels", "level4.txt")
]

level_index = 0




def load_current_level():

    global level
    global walls
    global goals
    global boxes
    global player

    global screen
    global screen_width
    global screen_height

    level, walls, goals, boxes, player = load_level(levels[level_index])

    if player is not None and not isinstance(player, tuple):
        player = tuple(player)

    map_width = len(level[0]) * TILE
    map_height = len(level) * TILE

    GAP = 120

    screen_width = map_width + PANEL + GAP
    screen_height = max(map_height, 760)

    screen = pygame.display.set_mode((screen_width, screen_height))

    return map_width


map_width = load_current_level()

pygame.display.set_caption("Sokoban AI")

clock = pygame.time.Clock()
running = True



message = ""

current_algo = "-"

expanded_nodes = 0
path_length = 0
path_cost = 0
search_time = 0

compare_results = []




def create_buttons():

    panel_x = screen_width - PANEL + 135

    return [
        Button(panel_x, 60, 110, 24, "BFS"),
        Button(panel_x, 95, 110, 24, "UCS"),
        Button(panel_x, 130, 110, 24, "IDS"),
        Button(panel_x, 165, 110, 24, "A*"),
        Button(panel_x, 200, 110, 24, "COMPARE"),
        Button(panel_x, 235, 110, 24, "RESET"),
        Button(panel_x, 270, 110, 24, "NEXT"),
        Button(panel_x, 305, 110, 24, "PREV"),
    ]


buttons = create_buttons()




def animate(path):

    global player
    global boxes
    global running

    if not path:
        return

    move_map = {
        (0,-1): "U",
        (0,1): "D",
        (-1,0): "L",
        (1,0): "R"
    }

    for step in path:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                return

        direction = move_map[step]

        player, boxes = move_player(
            player,
            boxes,
            direction,
            walls
        )

        draw_game(
            screen,
            level,
            walls,
            goals,
            boxes,
            player,
            buttons,
            current_algo,
            expanded_nodes,
            path_length,
            path_cost,
            search_time,
            compare_results,
            message
        )

        pygame.display.update()

        pygame.time.delay(120)




def run_solver(name):

    global current_algo
    global expanded_nodes
    global path_length
    global path_cost
    global search_time
    global message

    load_current_level()

    current_algo = name

    start = time.time()

    if name == "BFS":
        path, expanded = solve_bfs(player, boxes, walls, goals)

    elif name == "UCS":
        path, expanded = solve_ucs(player, boxes, walls, goals)

    elif name == "IDS":
        path, expanded = solve_ids(player, boxes, walls, goals)

    elif name == "A*":
        path, expanded = solve_astar(player, boxes, walls, goals)

    search_time = time.time() - start

    expanded_nodes = expanded

    if path is None:

        path_length = 0
        path_cost = 0

        message = "No Solution!"
        return

    path_length = len(path)

    path_cost = len(path)

    message = f"{name} Solved"

    animate(path)

    if is_goal(boxes, goals):
        message = "Level Complete!"




def compare_algorithms():

    global compare_results
    global message

    compare_results = []

    algorithms = [
        ("BFS", solve_bfs),
        ("UCS", solve_ucs),
        ("IDS", solve_ids),
        ("A*", solve_astar)
    ]

    for name, algo in algorithms:

        start = time.time()

        path, expanded = algo(
            player,
            boxes,
            walls,
            goals
        )

        elapsed = time.time() - start

        if path is None:
            steps = 0
            cost = 0
        else:
            steps = len(path)
            cost = len(path)

        compare_results.append({
            "name": name,
            "steps": steps,
            "expanded": expanded,
            "cost": cost,
            "time": elapsed
        })

    message = "Comparison Done"



while running:

    buttons = create_buttons()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False


        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_UP:
                player, boxes = move_player(player, boxes, "U", walls)

            elif event.key == pygame.K_DOWN:
                player, boxes = move_player(player, boxes, "D", walls)

            elif event.key == pygame.K_LEFT:
                player, boxes = move_player(player, boxes, "L", walls)

            elif event.key == pygame.K_RIGHT:
                player, boxes = move_player(player, boxes, "R", walls)

            elif event.key == pygame.K_b:
                run_solver("BFS")

            elif event.key == pygame.K_u:
                run_solver("UCS")

            elif event.key == pygame.K_i:
                run_solver("IDS")

            elif event.key == pygame.K_a:
                run_solver("A*")

            elif event.key == pygame.K_c:
                compare_algorithms()

            elif event.key == pygame.K_r:
                map_width = load_current_level()

            elif event.key == pygame.K_n:
                level_index = (level_index + 1) % len(levels)
                map_width = load_current_level()

            elif event.key == pygame.K_p:
                level_index = (level_index - 1) % len(levels)
                map_width = load_current_level()

            if player is not None and not isinstance(player, tuple):
                player = tuple(player)

       

        if event.type == pygame.MOUSEBUTTONDOWN:

            pos = pygame.mouse.get_pos()

            if buttons[0].clicked(pos):
                run_solver("BFS")

            elif buttons[1].clicked(pos):
                run_solver("UCS")

            elif buttons[2].clicked(pos):
                run_solver("IDS")

            elif buttons[3].clicked(pos):
                run_solver("A*")

            elif buttons[4].clicked(pos):
                compare_algorithms()

            elif buttons[5].clicked(pos):
                map_width = load_current_level()

            elif buttons[6].clicked(pos):
                level_index = (level_index + 1) % len(levels)
                map_width = load_current_level()

            elif buttons[7].clicked(pos):
                level_index = (level_index - 1) % len(levels)
                map_width = load_current_level()

    if is_goal(boxes, goals):
        message = "Level Complete!"

    if player is not None and not isinstance(player, tuple):
        player = tuple(player)

    draw_game(
        screen,
        level,
        walls,
        goals,
        boxes,
        player,
        buttons,
        current_algo,
        expanded_nodes,
        path_length,
        path_cost,
        search_time,
        compare_results,
        message
    )

    pygame.display.update()
    clock.tick(60)

pygame.quit()
