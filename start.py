# Menu: pick a game mode, play it in the same window, and come back here with Esc.

import pygame as p

import game_ui as ui

# (card, title, description, what you do, accent colour, game mode)
CARDS = [
    (p.Rect(50, 225, 270, 200), "Vs AI (attacker)", "The AI attacks. Stop it from making five in a row.",
     "You defend", ui.DEFEND, "vs_ai_attacker"),
    (p.Rect(365, 225, 270, 200), "2 Player", "Play a friend: one attacks, the other defends.",
     "Take turns", ui.HIGHLIGHT, "two_player"),
    (p.Rect(680, 225, 270, 200), "Vs AI (defender)", "The AI defends. Get five in a row before the board fills up.",
     "You attack", ui.ATTACK, "vs_ai_defender"),
]
HOW_TO_RECT = p.Rect(50, 465, 900, 270)


def set_cursor(hand):
    try:
        p.mouse.set_cursor(p.SYSTEM_CURSOR_HAND if hand else p.SYSTEM_CURSOR_ARROW)
    except p.error:
        pass   # some systems have no cursor support


def draw_title(screen):
    left = ui.text("Double Ball ", 56, ui.TEXT, True)
    right = ui.text("Gomoku", 56, ui.HIGHLIGHT, True)
    x = (ui.WIDTH - left.get_width() - right.get_width()) // 2
    screen.blit(left, (x, 70))
    screen.blit(right, (x + left.get_width(), 70))
    ui.draw_stone(screen, 1, (x - 40, 112), ui.SHADOW)
    ui.draw_stone(screen, 2, (x + left.get_width() + right.get_width() + 40, 112), ui.SHADOW)
    subtitle = ui.text("Five in a row, where every stone can help either side", 20, ui.MUTED)
    screen.blit(subtitle, subtitle.get_rect(center=(ui.WIDTH // 2, 172)))


def draw_card(screen, rect, title, description, tag, colour, hover):
    rect = rect.move(0, -4) if hover else rect
    p.draw.rect(screen, ui.SHADOW, rect.move(0, 6), border_radius=14)
    p.draw.rect(screen, ui.CARD_HI if hover else ui.PANEL, rect, border_radius=14)
    p.draw.rect(screen, colour if hover else ui.CARD, rect, 2, border_radius=14)
    p.draw.rect(screen, colour, (rect.x + 20, rect.y + 20, 36, 5), border_radius=3)
    screen.blit(ui.text(title, 24, ui.TEXT, True), (rect.x + 20, rect.y + 34))
    y = rect.y + 76
    for line in ui.wrap(description, 17, rect.width - 40):
        screen.blit(ui.text(line, 17, ui.MUTED), (rect.x + 20, y))
        y += 23
    label = ui.text(tag, 16, ui.BG, True)
    pill = label.get_rect(bottomleft=(rect.x + 20, rect.bottom - 20)).inflate(24, 10)
    pill.bottomleft = (rect.x + 20, rect.bottom - 18)
    p.draw.rect(screen, colour, pill, border_radius=pill.height // 2)
    screen.blit(label, label.get_rect(center=pill.center))


def draw_how_to(screen):
    p.draw.rect(screen, ui.PANEL, HOW_TO_RECT, border_radius=14)
    x, y = HOW_TO_RECT.x + 30, HOW_TO_RECT.y + 24
    ui.draw_section_label(screen, "HOW TO PLAY", x, y)
    ui.draw_rules(screen, x, y + 28, 470, size=18, line_height=25, gap=10)

    x = HOW_TO_RECT.x + 580
    ui.draw_section_label(screen, "CONTROLS", x, y)
    y = ui.draw_controls(screen, x, y + 28)
    ui.draw_section_label(screen, "IN A GAME", x, y + 10)
    for i, (key, what) in enumerate((("R", "new game"), ("Esc", "back to this menu"))):
        screen.blit(ui.text(key, 17, ui.TEXT, True), (x, y + 38 + i * 28))
        screen.blit(ui.text(what, 17, ui.MUTED), (x + 48, y + 38 + i * 28))


def menu(screen):
    # shows the menu until a mode is picked; returns the mode, or None if the window is closed
    clock = p.time.Clock()
    hand = None
    while True:
        mouse = p.mouse.get_pos()
        hovered = None
        for card in CARDS:
            if card[0].collidepoint(mouse):
                hovered = card[5]

        for e in p.event.get():
            if e.type == p.QUIT:
                set_cursor(False)
                return None
            if e.type == p.MOUSEBUTTONDOWN and e.button == 1:
                for rect, *_, mode in CARDS:
                    if rect.collidepoint(e.pos):
                        set_cursor(False)
                        return mode

        screen.fill(ui.BG)
        draw_title(screen)
        for rect, title, description, tag, colour, mode in CARDS:
            draw_card(screen, rect, title, description, tag, colour, hovered == mode)
        draw_how_to(screen)
        footer = ui.text("Click a mode to start", 16, ui.MUTED)
        screen.blit(footer, footer.get_rect(center=(ui.WIDTH // 2, 768)))
        if (hovered is not None) != hand:
            hand = hovered is not None
            set_cursor(hand)
        p.display.update()
        clock.tick(60)


def main():
    screen = ui.open_window()
    while True:
        mode = menu(screen)
        if mode is None:
            break
        _, _, action = ui.play(mode, screen, from_menu=True)
        if action == "quit":
            break
    p.quit()


if __name__ == "__main__":
    main()
