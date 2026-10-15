# Board geometry and game rules shared by all game modes.

GRID_START = 50   # pixel position of the board's top-left corner
CELL_SIZE = 40    # pixels per square
BOARD_SIZE = 15   # squares per side

DIRECTIONS = ((0, 1), (1, 0), (1, 1), (1, -1))   # horizontal, vertical, diagonal ↘, diagonal ↙


def pos_to_cell(pos):
    # mouse position -> (row, col) on the board, or None if the click is outside the grid
    col = (pos[0] - GRID_START) // CELL_SIZE
    row = (pos[1] - GRID_START) // CELL_SIZE
    if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
        return row, col
    return None


def win(arr):
    # True if five identical stones (either colour) are in a line anywhere on the board
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            v = arr[r][c]
            if v == 0:
                continue
            for dr, dc in DIRECTIONS:
                end_r, end_c = r + 4*dr, c + 4*dc
                if 0 <= end_r < BOARD_SIZE and 0 <= end_c < BOARD_SIZE and \
                        all(arr[r + i*dr][c + i*dc] == v for i in range(1, 5)):
                    return True
    return False


def result(arr):
    # game rules: any five in a row (either colour) -> attacker wins,
    # board full without a five -> defender wins, otherwise the game goes on (None)
    if win(arr):
        return "attacker"
    if not (arr == 0).any():
        return "defender"
    return None


def result_message(res):
    if res == "attacker":
        return "Attacker wins!"
    return "Defender wins! (board full)"
