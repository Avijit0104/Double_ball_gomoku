# Attacker AI.
#
# Tries every empty cell with both colours and scores how much "danger" (see ai_eval.py) the move
# adds. For the best candidates it also assumes the defender's best reply: a move that still leaves
# a five to complete after any reply (e.g. two threats at once) wins, so it scores highest.

import random

import numpy as np

from ai_eval import Board, FIVE, SIZE

CANDIDATES = 20        # how many of the best moves get the look-ahead check
WIN_NEXT = FIVE // 2   # bonus when the defender cannot stop a five on the next move


def _reply_value(board, r, c, v):
    # value for the attacker after the defender places colour v at (r, c)
    gain, fours_change = board.effect(r, c, v)
    if gain >= FIVE // 2:                 # the defender completed a five itself
        return FIVE
    if board.fours + fours_change > 0:    # a five is still open for the attacker's next move
        return gain + WIN_NEXT
    return gain


def aiattack(game_array):
    new_arr = game_array.copy()
    board = Board(game_array)
    empty = board.empty_cells()
    if not empty:
        return new_arr
    if len(empty) == SIZE * SIZE:   # first move: centre of the board
        new_arr[SIZE // 2][SIZE // 2] = random.choice((1, 2))
        return new_arr

    # 1) how much danger each possible move adds (higher = better for the attacker)
    moves = [(board.gain(r, c, v), r, c, v) for r, c in empty for v in (1, 2)]
    random.shuffle(moves)   # vary the choice between equally good moves
    moves.sort(key=lambda m: m[0], reverse=True)

    # 2) completing five wins straight away
    g1, r, c, v = moves[0]
    if g1 >= FIVE // 2:
        new_arr[r][c] = v
        return new_arr

    # 3) for the best candidates, assume the defender's best reply
    best_score, best_move = None, None
    for g1, r, c, v in moves[:CANDIDATES]:
        board.place(r, c, v)
        worst = min((_reply_value(board, rr, cc, vv) for rr, cc in empty if (rr, cc) != (r, c) for vv in (1, 2)), default=0)
        board.place(r, c, v, -1)
        score = g1 + worst
        if best_score is None or score > best_score:
            best_score, best_move = score, (r, c, v)

    r, c, v = best_move
    new_arr[r][c] = v
    return new_arr


if __name__ == "__main__":
    # small demo: two white stones on a diagonal
    game_array = np.zeros((15, 15), dtype=int)
    game_array[10][10] = game_array[11][11] = 1
    print(game_array)
    new_arr = aiattack(game_array)
    (r, c), = np.argwhere(new_arr != game_array)
    print(f"attacker plays colour {new_arr[r][c]} at row {r}, col {c}")
