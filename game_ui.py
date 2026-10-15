# Game window shared by all modes: look and feel, drawing, mouse/keyboard input, turns and the AI players.

import os
from functools import lru_cache

import numpy as np
import pygame as p

import ai_attacker
import ai_move
import game_arr as g

HERE = os.path.dirname(os.path.abspath(__file__))

WIDTH, HEIGHT = 1000, 800
AI_DELAY_MS = 500   # short pause before an AI move, so the human's stone is seen first

# colours
BG = (24, 28, 38)
PANEL = (36, 42, 56)
CARD = (46, 53, 70)
CARD_HI = (60, 69, 92)
TEXT = (236, 239, 244)
MUTED = (150, 158, 176)
WOOD = (224, 182, 118)
WOOD_EDGE = (178, 130, 74)
WOOD_SHADOW = (172, 128, 72)
GRID = (122, 84, 44)
SHADOW = (14, 16, 22)
ATTACK = (240, 112, 86)      # attacker accent
DEFEND = (86, 164, 255)      # defender accent
HIGHLIGHT = (255, 210, 60)   # last move, winning line, title
WHITE_STONE = (250, 250, 250)
BLACK_STONE = (78, 78, 84)   # shows through the black ball's seams

ROLE_COLOUR = {"attacker": ATTACK, "defender": DEFEND}

GRID_END = g.GRID_START + g.BOARD_SIZE * g.CELL_SIZE
BOARD_RECT = p.Rect(g.GRID_START - 20, g.GRID_START - 20, GRID_END - g.GRID_START + 40, GRID_END - g.GRID_START + 40)
PANEL_RECT = p.Rect(700, 30, 270, 740)
STATUS_Y = 722   # centre of the status message under the board

RULES = [
    "Each turn, place a stone of either colour.",
    "Attacker wins with any 5 in a row of one colour: across, down or diagonal.",
    "Defender wins if the board fills up with no five.",
    "The attacker always moves first.",
]
CONTROLS = [(1, "Left click", "white stone"), (2, "Right click", "black stone")]

# who plays each role in each mode, what they are called, and a one-line description
MODES = {
    "two_player":     {"attacker": "human", "defender": "human", "names": ("Player 1", "Player 2"),
                       "subtitle": "2 players, one computer"},
    "vs_ai_defender": {"attacker": "human", "defender": "ai", "names": ("You", "AI"),
                       "subtitle": "You attack, the AI defends"},
    "vs_ai_attacker": {"attacker": "ai", "defender": "human", "names": ("AI", "You"),
                       "subtitle": "The AI attacks, you defend"},
}
OTHER = {"attacker": "defender", "defender": "attacker"}


# ---------- text and images ----------

@lru_cache(maxsize=None)
def font(size, bold=False):
    # Segoe UI on Windows (pygame's name lookup picks its *light* variant, so the file is loaded
    # directly); otherwise a common sans-serif, or pygame's built-in font if none is installed
    path = os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts", "segoeuib.ttf" if bold else "segoeui.ttf")
    if os.path.exists(path):
        return p.font.Font(path, size)
    return p.font.SysFont("helvetica,arial,dejavusans,liberationsans", size, bold=bold)


@lru_cache(maxsize=1024)
def text(s, size, colour, bold=False):
    return font(size, bold).render(s, True, colour)


def wrap(s, size, width, bold=False):
    # split s into lines that fit in width pixels
    lines, line = [], ""
    for word in s.split():
        test = f"{line} {word}".strip()
        if font(size, bold).size(test)[0] <= width:
            line = test
        else:
            lines.append(line)
            line = word
    return lines + [line]


@lru_cache(maxsize=None)
def stone_images():
    return (p.image.load(os.path.join(HERE, "football.png")).convert_alpha(),
            p.image.load(os.path.join(HERE, "black.png")).convert_alpha())


def open_window():
    p.init()
    p.display.set_icon(p.image.load(os.path.join(HERE, "football.png")))
    screen = p.display.set_mode((WIDTH, HEIGHT))
    p.display.set_caption("Double Ball Gomoku")
    return screen


# ---------- drawing pieces ----------

def draw_stone(screen, value, center, shadow=WOOD_SHADOW):
    # a ball on a coloured disc (the images have see-through parts), with a soft shadow
    img = stone_images()[value - 1]
    radius = img.get_width() // 2
    x, y = center
    p.draw.circle(screen, shadow, (x + 2, y + 3), radius)
    p.draw.circle(screen, WHITE_STONE if value == 1 else BLACK_STONE, (x, y), radius - 1)
    screen.blit(img, img.get_rect(center=(x, y)))


def cell_center(row, col):
    return (g.GRID_START + col * g.CELL_SIZE + g.CELL_SIZE // 2,
            g.GRID_START + row * g.CELL_SIZE + g.CELL_SIZE // 2)


def draw_section_label(screen, label, x, y):
    screen.blit(text(label, 14, MUTED, True), (x, y))


def draw_rules(screen, x, y, width, size=16, line_height=21, gap=8):
    # the rules as a bullet list; returns the y below the last line
    for rule in RULES:
        p.draw.circle(screen, HIGHLIGHT, (x + 4, y + line_height // 2 + 1), 3)
        for line in wrap(rule, size, width - 16):
            screen.blit(text(line, size, TEXT), (x + 16, y))
            y += line_height
        y += gap
    return y


def draw_controls(screen, x, y, shadow=SHADOW):
    # stone icons with the mouse button that places them; returns the y below
    for value, button, what in CONTROLS:
        draw_stone(screen, value, (x + 16, y + 16), shadow)
        screen.blit(text(button, 17, TEXT, True), (x + 44, y + 4))
        screen.blit(text(what, 17, MUTED), (x + 44 + text(button, 17, TEXT, True).get_width() + 8, y + 4))
        y += 44
    return y


def draw_board(screen, game_array, last_move, win_cells, hover_cell, hover_colour):
    p.draw.rect(screen, SHADOW, BOARD_RECT.move(6, 8), border_radius=14)
    p.draw.rect(screen, WOOD, BOARD_RECT, border_radius=14)
    p.draw.rect(screen, WOOD_EDGE, BOARD_RECT, 3, border_radius=14)
    for i in range(g.BOARD_SIZE + 1):
        x = g.GRID_START + i * g.CELL_SIZE
        width = 2 if i in (0, g.BOARD_SIZE) else 1
        p.draw.line(screen, GRID, (x, g.GRID_START), (x, GRID_END), width)
        p.draw.line(screen, GRID, (g.GRID_START, x), (GRID_END, x), width)

    # where the next stone would go
    if hover_cell is not None:
        ring = p.Surface((g.CELL_SIZE, g.CELL_SIZE), p.SRCALPHA)
        p.draw.circle(ring, (*hover_colour, 170), (g.CELL_SIZE // 2, g.CELL_SIZE // 2), 15, 3)
        screen.blit(ring, (g.GRID_START + hover_cell[1] * g.CELL_SIZE, g.GRID_START + hover_cell[0] * g.CELL_SIZE))

    for row, col in np.argwhere(game_array != 0):
        draw_stone(screen, int(game_array[row][col]), cell_center(row, col))

    if last_move is not None and win_cells is None:
        p.draw.circle(screen, HIGHLIGHT, cell_center(*last_move), 19, 3)

    if win_cells is not None:
        overlay = p.Surface((WIDTH, HEIGHT), p.SRCALPHA)
        start, end = cell_center(*win_cells[0]), cell_center(*win_cells[-1])
        p.draw.line(overlay, (*HIGHLIGHT, 150), start, end, 10)
        for point in (start, end):
            p.draw.circle(overlay, (*HIGHLIGHT, 150), point, 5)
        screen.blit(overlay, (0, 0))
        for cell in win_cells:
            p.draw.circle(screen, HIGHLIGHT, cell_center(*cell), 19, 3)


def draw_role_card(screen, rect, role, name, active, tag, tag_colour):
    colour = ROLE_COLOUR[role]
    p.draw.rect(screen, CARD_HI if active else CARD, rect, border_radius=10)
    if active:
        p.draw.rect(screen, colour, rect, 2, border_radius=10)
    p.draw.rect(screen, colour, (rect.x, rect.y, 6, rect.height), border_top_left_radius=10, border_bottom_left_radius=10)
    screen.blit(text(role.capitalize(), 20, TEXT, True), (rect.x + 18, rect.y + 5))
    screen.blit(text(name, 16, MUTED), (rect.x + 18, rect.y + 31))
    if tag:
        label = text(tag, 15, tag_colour, True)
        screen.blit(label, label.get_rect(midright=(rect.right - 12, rect.centery)))


def draw_panel(screen, mode, turn, res, thinking, stones_placed, from_menu):
    info = MODES[mode]
    p.draw.rect(screen, PANEL, PANEL_RECT, border_radius=16)
    x, right = PANEL_RECT.x + 22, PANEL_RECT.right - 22
    width = right - x

    screen.blit(text("Double Ball", 30, TEXT, True), (x, PANEL_RECT.y + 16))
    screen.blit(text("Gomoku", 30, HIGHLIGHT, True), (x, PANEL_RECT.y + 52))
    screen.blit(text(info["subtitle"], 16, MUTED), (x, PANEL_RECT.y + 96))

    y = PANEL_RECT.y + 134
    draw_section_label(screen, "TURN", x, y)
    for i, role in enumerate(("attacker", "defender")):
        active = res is None and turn == role
        if res == role:
            tag, tag_colour = "WINNER", HIGHLIGHT
        elif active:
            tag, tag_colour = ("thinking..." if thinking else "to move"), ROLE_COLOUR[role]
        else:
            tag, tag_colour = "", MUTED
        draw_role_card(screen, p.Rect(x, y + 24 + i * 64, width, 56), role, info["names"][i], active, tag, tag_colour)

    y += 24 + 2 * 64 + 14
    draw_section_label(screen, "CONTROLS", x, y)
    y = draw_controls(screen, x, y + 24)

    y += 6
    draw_section_label(screen, "RULES", x, y)
    draw_rules(screen, x, y + 24, width)

    # footer
    footer_y = PANEL_RECT.bottom - 58
    p.draw.line(screen, CARD, (x, footer_y - 10), (right, footer_y - 10), 1)
    screen.blit(text(f"Stones placed: {stones_placed} / {g.BOARD_SIZE ** 2}", 15, MUTED), (x, footer_y))
    keys = "R  new game" + ("     Esc  menu" if from_menu else "")
    screen.blit(text(keys, 15, MUTED, True), (x, footer_y + 22))


def draw_status(screen, mode, turn, res, thinking, from_menu):
    # the message under the board
    info = MODES[mode]
    if res is not None:
        message, colour = g.result_message(res), ROLE_COLOUR[res]
        hint = "Press R to play again" + (" or Esc for the menu" if from_menu else "")
    elif thinking:
        message, colour = "AI is thinking...", MUTED
        hint = ""
    else:
        name = info["names"][0 if turn == "attacker" else 1]
        message = "Your move" if name == "You" else f"{name}'s move ({turn})"
        colour = ROLE_COLOUR[turn]
        hint = "Left click: white stone    Right click: black stone"

    label = text(message, 24, colour, True)
    pill = label.get_rect(center=((g.GRID_START + GRID_END) // 2, STATUS_Y)).inflate(44, 16)
    p.draw.rect(screen, PANEL, pill, border_radius=pill.height // 2)
    p.draw.rect(screen, colour, pill, 2, border_radius=pill.height // 2)
    screen.blit(label, label.get_rect(center=pill.center))
    if hint:
        hint_label = text(hint, 15, MUTED)
        screen.blit(hint_label, hint_label.get_rect(center=(pill.centerx, pill.bottom + 16)))


def draw(screen, mode, game_array, turn, res, last_move, win_cells, thinking, from_menu, mouse_pos):
    screen.fill(BG)
    hover_cell = None
    if res is None and not thinking and MODES[mode][turn] == "human":
        cell = g.pos_to_cell(mouse_pos)
        if cell is not None and game_array[cell[0]][cell[1]] == 0:
            hover_cell = cell
    draw_board(screen, game_array, last_move, win_cells, hover_cell, ROLE_COLOUR[turn])
    draw_panel(screen, mode, turn, res, thinking, int(np.count_nonzero(game_array)), from_menu)
    draw_status(screen, mode, turn, res, thinking, from_menu)


# ---------- game logic ----------

def ai_move_for(role, game_array):
    if role == "attacker":
        return ai_attacker.aiattack(game_array)
    new_arr, _, _ = ai_move.aimove(game_array)
    return new_arr


def place_stone(game_array, pos, button):
    # left click = white (1), right click = black (2); returns the (row, col) placed, or None
    cell = g.pos_to_cell(pos)
    if cell is None or button not in (1, 3):
        return None
    row, col = cell
    if game_array[row][col] != 0:
        return None
    game_array[row][col] = 1 if button == 1 else 2
    return cell


def play(mode, screen=None, board=None, from_menu=False):
    # runs one game until the window is closed (or Esc, if started from the menu);
    # returns (final board, result, "quit" or "menu").
    # board = optional start position (used for testing)
    players = MODES[mode]
    if screen is None:
        screen = open_window()
    clock = p.time.Clock()

    def new_game():
        start = np.zeros((g.BOARD_SIZE, g.BOARD_SIZE), dtype=int) if board is None else board.copy()
        return start, "attacker", None   # board, whose turn (attacker first), last move

    def check(game_array):
        res = g.result(game_array)
        return res, (g.winning_line(game_array) if res == "attacker" else None)

    game_array, turn, last_move = new_game()
    res, win_cells = check(game_array)

    while True:
        for e in p.event.get():
            if e.type == p.QUIT:
                return game_array, res, "quit"
            if e.type == p.KEYDOWN:
                if e.key == p.K_r:
                    game_array, turn, last_move = new_game()
                    res, win_cells = check(game_array)
                elif e.key == p.K_ESCAPE and from_menu:
                    return game_array, res, "menu"
            elif e.type == p.MOUSEBUTTONDOWN and res is None and players[turn] == "human":
                cell = place_stone(game_array, e.pos, e.button)
                if cell is not None:
                    last_move, turn = cell, OTHER[turn]
                    res, win_cells = check(game_array)

        ai_turn = res is None and players[turn] == "ai"
        draw(screen, mode, game_array, turn, res, last_move, win_cells, ai_turn, from_menu, p.mouse.get_pos())
        p.display.update()

        if ai_turn:
            p.time.delay(AI_DELAY_MS)
            new_arr = ai_move_for(turn, game_array)
            last_move = tuple(int(v) for v in np.argwhere(new_arr != game_array)[0])
            game_array, turn = new_arr, OTHER[turn]
            res, win_cells = check(game_array)
            p.event.clear(p.MOUSEBUTTONDOWN)   # ignore clicks made while the AI was thinking

        clock.tick(60)
