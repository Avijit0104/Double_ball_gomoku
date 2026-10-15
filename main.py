import pygame as p
import numpy as np
import game_arr as g


# print(__name__)


game_array = np.zeros((15,15),dtype=int)


p.init()
scr=p.display.set_mode((1000,800))
run=True
font = p.font.SysFont(None, 48)  
font_player = p.font.SysFont(None, 35)  

w_b = p.image.load("football.png")
wbx , wby = 750 , 300
b_b = p.image.load("black.png")
bbx , bby = 750 , 350
def w_ball(x=wbx,y=wby):
    scr.blit(w_b,(x,y))
def b_ball(x=bbx,y=bby):
    scr.blit(b_b,(x,y))

placed = []

win=False
running = True



turn = "p1"

while run:


    scr.fill((15, 212, 176))
    # scr.fill((255,255,255))
    w_ball()
    b_ball()
    
    for i in range(16):
        x=50 + (i*40)
        p.draw.line(scr,(0,0,0),(x,50),(x,650),2)

    for i in range(16):
        y=50 + (i*40)
        p.draw.line(scr,(0,0,0),(50,y),(650,y),2)

    p.draw.line(scr,(0,0,0),(700,0),(700,800),5)
    
    
    
    # Player 1 box (fixed role: attacker, moves first)
    box = p.Rect(750,150,200,30)
    if turn == "p1":
        p.draw.rect(scr, (200,200,200), box)  # active (grey)
    else:
        p.draw.rect(scr, (15, 212, 176), box) # inactive (green)
    p.draw.rect(scr, (0,0,0), box, 3)
    p1 = font_player.render("Attacker (P1)", True, (0, 0, 0))
    scr.blit(p1, (760, 151))

    # Player 2 box (fixed role: defender)
    box2 = p.Rect(750,190,200,30)
    if turn == "p2":
        p.draw.rect(scr, (200,200,200), box2)  # active (grey)
    else:
        p.draw.rect(scr, (15, 212, 176), box2) # inactive (green)
    p.draw.rect(scr, (0,0,0), box2, 3)
    p2 = font_player.render("Defender (P2)", True, (0, 0, 0))
    scr.blit(p2, (760, 191))

    for row, col, t in placed:
        cell_x = 50 + col * 40
        cell_y = 50 + row * 40
        if t == 1:
            scr.blit(w_b, (cell_x, cell_y))
        else:
            scr.blit(b_b, (cell_x, cell_y))

    # pos = p.mouse.get_pos()
    # print(pos)
    for e in p.event.get():
        if e.type == p.QUIT:
            run=False
        if e.type == p.MOUSEBUTTONDOWN:
            if running :
                # if turn == "p1":
                #     box = p.Rect(750,150,110,30)
                #     p.draw.rect(scr,(200,200,200),box)
                #     p.draw.rect(scr,(0,0,0),box,3)

                #     p1 = font_player.render("player 1", True, (0, 0, 0))
                #     scr.blit(p1, (760, 151))
                #     print(turn)
                #     turn="p2"

                # elif turn == "p2":
                #     box2 = p.Rect(880,150,110,30)
                #     p.draw.rect(scr,(15, 212, 176),box2)
                #     p.draw.rect(scr,(0,0,0),box2,3)

                #     p2 = font_player.render("player 2", True, (0, 0, 0))
                #     scr.blit(p2, (890, 151))
                #     print(turn)
                #     turn="p1"
                




                # print(e) 
                butt = e.button
                pos = e.pos

                
                cell = g.pos_to_cell(pos)
                # only left (white) / right (black) click places a stone; other buttons don't use up the turn
                if cell is not None and butt in (1, 3):
                    print(pos)
                    print(butt)
                    row, col = cell

                    cell_x = 50 + col * 40
                    cell_y = 50 + row * 40

                    if game_array[row][col] == 0:  # only place if empty
                        if turn == "p1":
                            if butt == 1:
                                game_array[row][col] = 1
                                placed.append((row, col, 1))

                            elif butt == 3:
                                game_array[row][col] = 2
                                placed.append((row, col, 2))

                            
                            turn = "p2"
                        else:
                            if butt == 1:
                                game_array[row][col] = 1
                                placed.append((row, col, 1))

                            elif butt == 3:
                                game_array[row][col] = 2
                                placed.append((row, col, 2))
                            turn = "p1"

                        for row, col, t in placed:
                            cell_x = 50 + col * 40
                            cell_y = 50 + row * 40
                            if t == 1:
                                scr.blit(w_b, (cell_x, cell_y))
                            else:
                                scr.blit(b_b, (cell_x, cell_y))


    res = g.result(game_array)
    if res is not None:
        text_surface = font.render(g.result_message(res), True, (0, 0, 0), (200, 200, 200))
        scr.blit(text_surface, text_surface.get_rect(center=(350, 350)))
        running=False

    p.display.update()