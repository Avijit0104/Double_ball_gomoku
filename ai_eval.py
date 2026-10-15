# Position scoring shared by both AIs.
#
# Every 5-cell line on the board (a "window") is a place where a five could still appear.
# A window holding stones of only one colour scores by how many stones it has; a window holding
# both colours can never become five, so it is dead and scores 0. The sum over all windows is the
# board's "danger": the attacker wants it high, the defender wants it low.

SIZE = 15
WINDOW_SCORE = [0, 1, 10, 100, 1000]   # index = stones of one colour in a live window
FOUR = WINDOW_SCORE[4]                  # a live window one stone away from five
FIVE = 10**7                            # a window that is five in a row


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


def window_value(n1, n2):
    # n1, n2 = number of colour-1 and colour-2 stones in the window
    if n1 and n2:
        return 0
    n = n1 or n2
    return FIVE if n >= 5 else WINDOW_SCORE[n]


class Board:
    # board + stone counts per window, updated as moves are tried and taken back

    def __init__(self, arr):
        self.arr = [[int(v) for v in row] for row in arr]
        self.counts = []
        for cells in WINDOWS:
            vals = [self.arr[r][c] for r, c in cells]
            self.counts.append([vals.count(1), vals.count(2)])
        # live fours = windows where the attacker can complete five with the next stone
        self.fours = sum(window_value(n1, n2) == FOUR for n1, n2 in self.counts)

    def empty_cells(self):
        return [(r, c) for r in range(SIZE) for c in range(SIZE) if self.arr[r][c] == 0]

    def gain(self, r, c, v):
        # change in danger if colour v is placed at (r, c)
        gain = 0
        for w in CELL_WINDOWS[r][c]:
            n1, n2 = self.counts[w]
            gain += window_value(n1 + (v == 1), n2 + (v == 2)) - window_value(n1, n2)
        return gain

    def effect(self, r, c, v):
        # (change in danger, change in live fours) if colour v is placed at (r, c)
        gain = fours = 0
        for w in CELL_WINDOWS[r][c]:
            n1, n2 = self.counts[w]
            before = window_value(n1, n2)
            after = window_value(n1 + (v == 1), n2 + (v == 2))
            gain += after - before
            fours += (after == FOUR) - (before == FOUR)
        return gain, fours

    def place(self, r, c, v, step=1):
        # step = +1 places colour v at (r, c), -1 takes it back
        for w in CELL_WINDOWS[r][c]:
            n = self.counts[w]
            self.fours -= window_value(*n) == FOUR
            n[v - 1] += step
            self.fours += window_value(*n) == FOUR
        self.arr[r][c] = v if step > 0 else 0
