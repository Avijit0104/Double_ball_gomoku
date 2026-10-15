import numpy as np

GRID_START = 50
CELL_SIZE = 40
BOARD_SIZE = 15

def pos_to_cell(pos):
    # mouse position -> (row, col) on the board, or None if the click is outside the grid
    col = (pos[0] - GRID_START) // CELL_SIZE
    row = (pos[1] - GRID_START) // CELL_SIZE
    if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
        return row, col
    return None

def win(arr):



    #for horizontal checking
    for k in range(15):
        for i in range(11):
            if (arr[k][i] == 1 or arr[k][i] == 2):
                c=0
                for j in range(i+1,i+5):
                    if arr[k][i] == arr[k][j]:
                        c+=1
                    else:
                        break
                if c==4:
                    return True

    #for vertical checking
    for k in range(15):
        for i in range(11):
            if (arr[i][k] == 1 or arr[i][k] == 2):
                c=0
                for j in range(i+1,i+5):
                    if arr[i][k] == arr[j][k]:
                        c+=1
                    else:
                        break
                if c==4:
                    return True


    #for digonal_right checking
    for k in range(11):
        for i in range(11):
            if (arr[k][i] == 1 or arr[k][i] == 2):
                c=0
                for j in range(1,5):
                    if arr[k][i] == arr[k+j][i+j]:
                        c+=1
                    else:
                        break
                if c==4:
                    return True

    #for digonal_left checking
    for k in range(11):
        for i in range(14,3,-1):
            if (arr[k][i] == 1 or arr[k][i] == 2):
                c=0
                for j in range(1,5):
                    if arr[k][i] == arr[k+j][i-j]:
                        c+=1
                    else:
                        break
                if c==4:
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




# print("hi")
# print(__name__)

if (__name__ == "__main__"):
    game_array = np.zeros((15,15),dtype=int)
    # for i in range(10,15):
    #     game_array[i][i]=1
    # game_array[14][0]=2
    # game_array[13][1]=2
    # game_array[12][2]=2
    # game_array[11][3]=2
    # game_array[10][4]=2
    print(game_array)
    print(win(game_array))