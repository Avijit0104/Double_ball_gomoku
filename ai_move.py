# Defender AI.
#
# Tries every empty cell with both colours and scores how much "danger" (see ai_eval.py) the move
# leaves for the attacker. For the best candidates it also assumes the attacker's best reply, so
# moves that let the attacker complete five, or build a big threat, are avoided.

import random

import numpy as np

from ai_eval import Board

CANDIDATES = 20   # how many of the best moves get the look-ahead check


def aimove(game_array):
    # returns (new board, row, col); row and col are None if the board is full
    new_arr = game_array.copy()
    board = Board(game_array)
    empty = board.empty_cells()
    if not empty:
        return new_arr, None, None

    # 1) danger left after each possible defender move (lower = better for the defender)
    moves = sorted((board.gain(r, c, v), r, c, v) for r, c in empty for v in (1, 2))

    # 2) for the best candidates, add the attacker's best reply
    #    (a reply that completes five scores FIVE, so moves that allow it are avoided)
    best_score, best_moves = None, []
    for g1, r, c, v in moves[:CANDIDATES]:
        board.place(r, c, v)
        reply = max((board.gain(rr, cc, vv) for rr, cc in empty if (rr, cc) != (r, c) for vv in (1, 2)), default=0)
        board.place(r, c, v, -1)
        score = g1 + reply
        if best_score is None or score < best_score:
            best_score, best_moves = score, [(r, c, v)]
        elif score == best_score:
            best_moves.append((r, c, v))

    r, c, v = random.choice(best_moves)
    new_arr[r][c] = v
    return new_arr, r, c


if __name__ == "__main__":
    # small demo: the attacker has an open three of black stones in row 7
    game_array = np.zeros((15, 15), dtype=int)
    game_array[7][5:8] = 2
    print(game_array)
    new_arr, r, c = aimove(game_array)
    print(f"defender plays colour {new_arr[r][c]} at row {r}, col {c}")
