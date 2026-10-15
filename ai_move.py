import numpy as np
import random

def check(arr):
    sc_arr = np.zeros((15,15), dtype=int)

    # ----- Horizontal -----
    for r in range(15):
        c = 0
        for i in range(15):
            if i > 0 and arr[r][i] == arr[r][i-1] and arr[r][i] in [1,2]:
                c += 1
            else:
                if c >= 1:
                    for j in range(i-c-1, i):
                        sc_arr[r][j] = c+1
                c = 0
        if c >= 1:
            for j in range(15-c-1, 15):
                sc_arr[r][j] = c+1

    # ----- Vertical -----
    for c in range(15):
        k = 0
        for i in range(15):
            if i > 0 and arr[i][c] == arr[i-1][c] and arr[i][c] in [1,2]:
                k += 1
            else:
                if k >= 1:
                    for j in range(i-k-1, i):
                        sc_arr[j][c] = k+1
                k = 0
        if k >= 1:
            for j in range(15-k-1, 15):
                sc_arr[j][c] = k+1

    # ----- Diagonal ↘ -----
    for r in range(15):
        for c in range(15):
            if arr[r][c] in [1,2]:
                val = arr[r][c]
                count = 1
                x, y = r+1, c+1
                while x < 15 and y < 15 and arr[x][y] == val:
                    count += 1
                    x += 1
                    y += 1
                if count >= 2:
                    for p in range(count):
                        if r+p < 15 and c+p < 15:
                            sc_arr[r+p][c+p] = count

    # ----- Diagonal ↙ -----
    for r in range(15):
        for c in range(15):
            if arr[r][c] in [1,2]:
                val = arr[r][c]
                count = 1
                x, y = r+1, c-1
                while x < 15 and y >= 0 and arr[x][y] == val:
                    count += 1
                    x += 1
                    y -= 1
                if count >= 2:
                    for p in range(count):
                        if r+p < 15 and c-p >= 0:
                            sc_arr[r+p][c-p] = count

    return sc_arr


# ---------------- Defender AI ----------------
# Every 5-cell line on the board ("window") is a place where the attacker could still make five.
# A window holding only one colour scores by how many stones it has; a window holding both
# colours can never become five, so it is dead and scores 0.
# The defender tries every empty cell with both colours and picks the move that leaves the
# attacker the least danger, also looking one attacker reply ahead for its best candidates.

SIZE = 15
WINDOW_SCORE = [0, 1, 10, 100, 1000]   # index = stones of one colour in a live window
FIVE = 10**7                            # a window that is already five in a row
CANDIDATES = 20                         # how many of the best moves get the look-ahead check


def _build_windows():
    windows = []
    for r in range(SIZE):
        for c in range(SIZE):
            for dr, dc in ((0, 1), (1, 0), (1, 1), (1, -1)):
                if 0 <= r + 4*dr < SIZE and 0 <= c + 4*dc < SIZE:
                    windows.append([(r + i*dr, c + i*dc) for i in range(5)])
    cell_windows = [[[] for _ in range(SIZE)] for _ in range(SIZE)]
    for w, cells in enumerate(windows):
        for r, c in cells:
            cell_windows[r][c].append(w)
    return windows, cell_windows

WINDOWS, CELL_WINDOWS = _build_windows()


def _window_value(n1, n2):
    if n1 and n2:
        return 0
    n = n1 or n2
    return FIVE if n >= 5 else WINDOW_SCORE[n]


def _count_windows(arr):
    # counts[w] = [number of 1s, number of 2s] in window w
    counts = []
    for cells in WINDOWS:
        vals = [arr[r][c] for r, c in cells]
        counts.append([vals.count(1), vals.count(2)])
    return counts


def _gain(counts, r, c, v):
    # how much the attacker's danger score changes if colour v is placed at (r, c)
    gain = 0
    for w in CELL_WINDOWS[r][c]:
        n1, n2 = counts[w]
        gain += _window_value(n1 + (v == 1), n2 + (v == 2)) - _window_value(n1, n2)
    return gain


def _apply(counts, r, c, v, step):
    # step = +1 places colour v at (r, c), -1 takes it back
    for w in CELL_WINDOWS[r][c]:
        counts[w][v - 1] += step


def aimove(game_array, sc_array=None):
    # sc_array is no longer used (kept so old calls still work)
    new_arr = game_array.copy()
    empty = [(int(r), int(c)) for r, c in np.argwhere(game_array == 0)]
    if not empty:
        return new_arr, None, None   # board is full: no move possible

    counts = _count_windows(game_array)

    # 1) danger left after each possible defender move (lower = better for the defender)
    moves = sorted((_gain(counts, r, c, v), r, c, v) for r, c in empty for v in (1, 2))

    # 2) for the best candidates, add the attacker's best reply
    #    (a reply that completes five scores FIVE, so moves that allow it are avoided)
    best_score, best_moves = None, []
    for g1, r, c, v in moves[:CANDIDATES]:
        _apply(counts, r, c, v, +1)
        reply = max((_gain(counts, rr, cc, vv) for rr, cc in empty if (rr, cc) != (r, c) for vv in (1, 2)), default=0)
        _apply(counts, r, c, v, -1)
        score = g1 + reply
        if best_score is None or score < best_score:
            best_score, best_moves = score, [(r, c, v)]
        elif score == best_score:
            best_moves.append((r, c, v))

    r, c, v = random.choice(best_moves)
    new_arr[r][c] = v
    return new_arr, r, c


if (__name__ == "__main__"):
    game_array = np.zeros((15,15),dtype=int)
    # for i in range(10,12):
    #     game_array[i][i]=1
    game_array[14][0]=2
    game_array[13][1]=2
    game_array[12][2]=2
    game_array[10][3]=2
    game_array[11][4]=2
    print(game_array)
    print()
    sc_array=check(game_array)
    print(sc_array)
    print()
    print(aimove(game_array,sc_array))