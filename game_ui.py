# Game window shared by all modes: drawing, mouse input, turns and the AI players.

import os

import numpy as np
import pygame as p

import ai_attacker
import ai_move
import game_arr as g

HERE = os.path.dirname(os.path.abspath(__file__))

WIDTH, HEIGHT = 1000, 800
BG = (15, 212, 176)
BLACK = (0, 0, 0)
GREY = (200, 200, 200)
GRID_END = g.GRID_START + g.BOARD_SIZE * g.CELL_SIZE
AI_DELAY_MS = 500   # short pause before an AI move, so the human's stone is seen first

# who plays each role in each mode, and the labels shown in the side panel
MODES = {
    "two_player":     {"attacker": "human", "defender": "human", "labels": ("Attacker (P1)", "Defender (P2)")},
    "vs_ai_defender": {"attacker": "human", "defender": "ai",    "labels": ("Attacker (player)", "Defender (AI)")},
    "vs_ai_attacker": {"attacker": "ai",    "defender": "human", "labels": ("Attacker (AI)", "Defender (player)")},
}


def open_window():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    p.display.set_caption("Double Ball Gomoku")
    return screen


def ai_move_for(role, game_array):
    if role == "attacker":
        return ai_attacker.aiattack(game_array)
    new_arr, _, _ = ai_move.aimove(game_array)
    return new_arr


def place_stone(game_array, pos, button):
    # left click = white (1), right click = black (2); returns True if a stone was placed
    cell = g.pos_to_cell(pos)
    if cell is None or button not in (1, 3):
        return False
    row, col = cell
    if game_array[row][col] != 0:
        return False
    game_array[row][col] = 1 if button == 1 else 2
    return True


def draw(screen, fonts, stones, game_array, labels, turn, res):
    font, font_player = fonts
    white, black = stones
    screen.fill(BG)

    # board grid and the divider to the side panel
    for i in range(g.BOARD_SIZE + 1):
        x = g.GRID_START + i * g.CELL_SIZE
        p.draw.line(screen, BLACK, (x, g.GRID_START), (x, GRID_END), 2)
        p.draw.line(screen, BLACK, (g.GRID_START, x), (GRID_END, x), 2)
    p.draw.line(screen, BLACK, (700, 0), (700, HEIGHT), 5)

    # side panel: whose turn it is (grey box) and the two stone types
    for i, (role, label) in enumerate(zip(("attacker", "defender"), labels)):
        text = font_player.render(label, True, BLACK)
        box = p.Rect(750, 150 + 40 * i, text.get_width() + 20, 30)
        p.draw.rect(screen, GREY if turn == role else BG, box)
        p.draw.rect(screen, BLACK, box, 3)
        screen.blit(text, (760, 151 + 40 * i))
    screen.blit(white, (750, 300))
    screen.blit(black, (750, 350))

    # stones, centred in their squares
    for row, col in np.argwhere(game_array != 0):
        img = white if game_array[row][col] == 1 else black
        x = g.GRID_START + col * g.CELL_SIZE + (g.CELL_SIZE - img.get_width()) // 2
        y = g.GRID_START + row * g.CELL_SIZE + (g.CELL_SIZE - img.get_height()) // 2
        screen.blit(img, (x, y))

    # result below the board, so the winning line stays visible
    if res is not None:
        text = font.render(g.result_message(res), True, BLACK, GREY)
        screen.blit(text, text.get_rect(center=((g.GRID_START + GRID_END) // 2, (GRID_END + HEIGHT) // 2)))


def play(mode, screen=None, board=None):
    # runs one game until the window is closed; returns the final board and result
    # (board lets a game start from a given position, used for testing)
    players = MODES[mode]
    if screen is None:
        screen = open_window()
    fonts = (p.font.SysFont(None, 48), p.font.SysFont(None, 35))
    stones = (p.image.load(os.path.join(HERE, "football.png")),
              p.image.load(os.path.join(HERE, "black.png")))
    clock = p.time.Clock()

    game_array = np.zeros((g.BOARD_SIZE, g.BOARD_SIZE), dtype=int) if board is None else board.copy()
    turn = "attacker"   # the attacker always moves first
    res = g.result(game_array)
    other = {"attacker": "defender", "defender": "attacker"}

    run = True
    while run:
        for e in p.event.get():
            if e.type == p.QUIT:
                run = False
            elif e.type == p.MOUSEBUTTONDOWN and res is None and players[turn] == "human":
                if place_stone(game_array, e.pos, e.button):
                    turn = other[turn]
                    res = g.result(game_array)

        draw(screen, fonts, stones, game_array, players["labels"], turn, res)
        p.display.update()

        if run and res is None and players[turn] == "ai":
            p.time.delay(AI_DELAY_MS)
            game_array = ai_move_for(turn, game_array)
            turn = other[turn]
            res = g.result(game_array)

        clock.tick(60)

    return game_array, res
