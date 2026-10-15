import numpy as np
import random

def aiattack(game_array):
    """
    Offensive AI: tries to extend sequences to 5 (offense).
    If 1–4 consecutive 2s → place 2 to extend.
    If 1–4 consecutive 1s → place 1 to extend.
    Prioritizes longer sequences first (4→3→2→1).
    If no extension possible, picks a random empty cell near existing pieces.
    """
    new_arr = game_array.copy()
    rows, cols = game_array.shape

    for length in [4, 3, 2, 1]:
        # ----- Horizontal -----
        for r in range(rows):
            for c in range(cols - 4):
                segment = list(game_array[r, c:c+5])
                for val in (2, 1):
                    if segment.count(val) == length:
                        idxs = [i for i, x in enumerate(segment) if x == val]

                        left = min(idxs) - 1
                        if 0 <= left < 5 and segment[left] == 0:
                            new_arr[r, c + left] = val
                            return new_arr

                        right = max(idxs) + 1
                        if 0 <= right < 5 and segment[right] == 0:
                            new_arr[r, c + right] = val
                            return new_arr

                        for k in range(5):
                            if segment[k] == 0:
                                new_arr[r, c + k] = val
                                return new_arr

        # ----- Vertical -----
        for c in range(cols):
            for r in range(rows - 4):
                segment = list(game_array[r:r+5, c])
                for val in (2, 1):
                    if segment.count(val) == length:
                        idxs = [i for i, x in enumerate(segment) if x == val]

                        up = min(idxs) - 1
                        if 0 <= up < 5 and segment[up] == 0:
                            new_arr[r + up, c] = val
                            return new_arr

                        down = max(idxs) + 1
                        if 0 <= down < 5 and segment[down] == 0:
                            new_arr[r + down, c] = val
                            return new_arr

                        for k in range(5):
                            if segment[k] == 0:
                                new_arr[r + k, c] = val
                                return new_arr

        # ----- Diagonal ↘ -----
        for r in range(rows - 4):
            for c in range(cols - 4):
                diag = [game_array[r+i][c+i] for i in range(5)]
                for val in (2, 1):
                    if diag.count(val) == length:
                        idxs = [i for i, x in enumerate(diag) if x == val]

                        left = min(idxs) - 1
                        if 0 <= left < 5 and diag[left] == 0:
                            new_arr[r + left, c + left] = val
                            return new_arr

                        right = max(idxs) + 1
                        if 0 <= right < 5 and diag[right] == 0:
                            new_arr[r + right, c + right] = val
                            return new_arr

                        for k in range(5):
                            if diag[k] == 0:
                                new_arr[r + k, c + k] = val
                                return new_arr

        # ----- Diagonal ↙ -----
        for r in range(rows - 4):
            for c in range(4, cols):
                diag = [game_array[r+i][c-i] for i in range(5)]
                for val in (2, 1):
                    if diag.count(val) == length:
                        idxs = [i for i, x in enumerate(diag) if x == val]

                        left = min(idxs) - 1
                        if 0 <= left < 5 and diag[left] == 0:
                            new_arr[r + left, c - left] = val
                            return new_arr

                        right = max(idxs) + 1
                        if 0 <= right < 5 and diag[right] == 0:
                            new_arr[r + right, c - right] = val
                            return new_arr

                        for k in range(5):
                            if diag[k] == 0:
                                new_arr[r + k, c - k] = val
                                return new_arr

    # ---------- fallback: place near existing AI pieces ----------
    empty_cells = np.argwhere(game_array == 0)
    neighbor_candidates = []

    for (r, c) in empty_cells:
        # check 8 directions for any existing 1 or 2
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols:
                    if game_array[nr][nc] in [1, 2]:
                        neighbor_candidates.append(((r, c), game_array[nr][nc]))

    if neighbor_candidates:
        (r, c), val = random.choice(neighbor_candidates)
        new_arr[r, c] = val
        return new_arr

    # ---------- ultimate fallback: random empty ----------
    if len(empty_cells) > 0:
        r, c = random.choice(empty_cells)
        new_arr[r, c] = random.choice([1, 2])

    return new_arr




if (__name__ == "__main__"):
    game_array = np.zeros((15,15),dtype=int)
    for i in range(10,12):
        game_array[i][i]=1
    # game_array[14][0]=2
    # game_array[13][1]=2
    # game_array[12][2]=2
    # # game_array[10][3]=2
    # game_array[10][4]=2
    print(game_array)
    print()
    # sc_array=check(game_array)
    # print(sc_array)
    # print()
    print(aiattack(game_array))