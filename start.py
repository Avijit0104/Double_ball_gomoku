# Menu: pick a game mode, then play it in the same window.

import pygame as p

import game_ui

# (button, label, game mode)
BUTTONS = [
    (p.Rect(50, 250, 230, 50), "Vs AI (attacker)", "vs_ai_attacker"),
    (p.Rect(400, 250, 130, 50), "2 player", "two_player"),
    (p.Rect(650, 250, 240, 50), "Vs AI (defender)", "vs_ai_defender"),
]


def main():
    screen = game_ui.open_window()
    font = p.font.SysFont(None, 40)
    clock = p.time.Clock()

    mode = None
    run = True
    while run and mode is None:
        for e in p.event.get():
            if e.type == p.QUIT:
                run = False
            elif e.type == p.MOUSEBUTTONDOWN and e.button == 1:
                for box, _, button_mode in BUTTONS:
                    if box.collidepoint(e.pos):
                        mode = button_mode

        screen.fill(game_ui.BG)
        for box, label, _ in BUTTONS:
            p.draw.rect(screen, game_ui.GREY, box)
            screen.blit(font.render(label, True, game_ui.BLACK), (box.x + 10, box.y + 10))
        p.display.update()
        clock.tick(60)

    if mode is not None:
        game_ui.play(mode, screen)
    p.quit()


if __name__ == "__main__":
    main()
