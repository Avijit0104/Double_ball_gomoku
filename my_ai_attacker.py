import pygame as p
import numpy as np
import game_arr as g
import ai_attacker as ai


# --- Initialize Game ---
game_array = np.zeros((15, 15), dtype=int)
p.init()
scr = p.display.set_mode((1000, 800))
font = p.font.SysFont(None, 48)
font_player = p.font.SysFont(None, 35)

# --- Load Images ---
w_b = p.image.load("football.png")
b_b = p.image.load("black.png")


wbx , wby = 750 , 300

bbx , bby = 750 , 350
def w_ball(x=wbx,y=wby):
    scr.blit(w_b,(x,y))
def b_ball(x=bbx,y=bby):
    scr.blit(b_b,(x,y))

# --- Constants ---
GRID_START = 50
GRID_END = 650
CELL_SIZE = 40

# --- Variables ---
running = True
run = True
turn = "p1"  # p1 = AI, p2 = player

# --- Functions ---
def draw_board():
    scr.fill((15, 212, 176))
    # grid lines
    for i in range(16):
        x = GRID_START + (i * CELL_SIZE)
        y = GRID_START + (i * CELL_SIZE)
        p.draw.line(scr, (0, 0, 0), (x, GRID_START), (x, GRID_END), 2)
        p.draw.line(scr, (0, 0, 0), (GRID_START, y), (GRID_END, y), 2)

    p.draw.line(scr, (0, 0, 0), (700, 0), (700, 800), 5)

    # player indicators
    box1 = p.Rect(750, 150, 120, 30)
    box2 = p.Rect(750, 190, 220, 30)
    p.draw.rect(scr, (200, 200, 200) if turn == "p1" else (15, 212, 176), box1)
    p.draw.rect(scr, (0, 0, 0), box1, 3)
    p.draw.rect(scr, (200, 200, 200) if turn == "p2" else (15, 212, 176), box2)
    p.draw.rect(scr, (0, 0, 0), box2, 3)

    p1_text = font_player.render("Attacker", True, (0, 0, 0))
    p2_text = font_player.render("Defender(player)", True, (0, 0, 0))
    scr.blit(p1_text, (760, 151))
    scr.blit(p2_text, (760, 191))

def draw_pieces():
    for row in range(15):
        for col in range(15):
            x = GRID_START + col * CELL_SIZE
            y = GRID_START + row * CELL_SIZE
            if game_array[row][col] == 1:
                scr.blit(w_b, (x, y))
            elif game_array[row][col] == 2:
                scr.blit(b_b, (x, y))

# --- Game Loop ---
while run:
    draw_board()
    draw_pieces()
    w_ball()
    b_ball()


    # check for game over (five -> attacker wins, full board -> defender wins)
    res = g.result(game_array)
    if res is not None:
        text_surface = font.render(g.result_message(res), True, (0, 0, 0), (200, 200, 200))
        scr.blit(text_surface, text_surface.get_rect(center=(350, 350)))
        running = False

    


    # --- Handle Events ---
    for e in p.event.get():
        if e.type == p.QUIT:
            run = False

        if e.type == p.MOUSEBUTTONDOWN and running:
            
            if turn == "p2":  # Player’s turn
                pos = e.pos
                butt = e.button
            
                cell = g.pos_to_cell(pos)
                # only left (white) / right (black) click places a stone; other buttons don't use up the turn
                if cell is not None and butt in (1, 3):
                    row, col = cell
                    if game_array[row][col] == 0:
                        if butt == 1:
                            game_array[row][col] = 1  # player 2 = black
                        elif butt == 3:
                            game_array[row][col] = 2  # player 2 = black
                        turn = "p1"

    # --- AI TURN --- (only if the human's move didn't already end the game)
    if running and turn == "p1" and g.result(game_array) is None:
        p.time.delay(500)  # little delay for visual comfort
        game_array = ai.aiattack(game_array)
        # print("AI moved at:", airow, aicol)
        turn = "p2"

    p.display.update()
