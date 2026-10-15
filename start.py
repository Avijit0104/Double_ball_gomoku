import pygame as p
import os
import subprocess
import sys


p.init()
scr=p.display.set_mode((1000,800))
run=True
font = p.font.SysFont(None, 40)
running=True

# folder this file is in: the games load their images relative to it
HERE = os.path.dirname(os.path.abspath(__file__))

attacker_box = p.Rect(50,250,230,50)
defender_box = p.Rect(650,250,240,50)
two_player_box = p.Rect(400,250,130,50)


def launch(script):
    # run the game with the same Python as this menu (so the venv's pygame/numpy are used)
    p.quit()
    subprocess.call([sys.executable, script], cwd=HERE)
    sys.exit()


while run:
    scr.fill((15, 212, 176))

    #vs ai(attacker)
    p.draw.rect(scr,(200,200,200),attacker_box)
    vs_ai = font.render("Vs AI (attacker)", True, (0, 0, 0))
    scr.blit(vs_ai, (60, 260))

    #vs ai(defender)
    p.draw.rect(scr,(200,200,200),defender_box)
    vs_ai = font.render("Vs AI (defender)", True, (0, 0, 0))
    scr.blit(vs_ai, (660, 260))

    #2-player
    p.draw.rect(scr,(200,200,200),two_player_box)
    pl = font.render("2 player", True, (0, 0, 0))
    scr.blit(pl, (410, 260))


    for e in p.event.get():
        if e.type == p.QUIT:
            run=False
        if e.type == p.MOUSEBUTTONDOWN and e.button == 1 and running:
            if two_player_box.collidepoint(e.pos):
                launch("main.py")
            if defender_box.collidepoint(e.pos):
                launch("my_ai.py")
            if attacker_box.collidepoint(e.pos):
                launch("my_ai_attacker.py")

    p.display.update()

p.quit()
