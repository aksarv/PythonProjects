"""
Minimax plays connect 4
"""

import copy, random, pygame

test_board = [[0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0]]

def three_row(board):
    ones_counter = 0
    twos_counter = 0
    for j in range(6):
        for i in range(5):
            if str(board[j][i]) + str(board[j][i + 1]) + str(board[j][i + 2]) == "11":
                ones_counter += 1
            if str(board[j][i]) + str(board[j][i + 1]) + str(board[j][i + 2]) == "22":
                twos_counter += 1
    for j in range(4):
        for i in range(7):
            if str(board[j][i]) + str(board[j + 1][i]) + str(board[j + 2][i]) == "11":
                ones_counter += 1
            if str(board[j][i]) + str(board[j + 1][i]) + str(board[j + 2][i]) == "22":
                twos_counter += 1
    for j in range(4):
        for i in range(5):
            if str(board[j][i]) + str(board[j + 1][i + 1]) + str(board[j + 2][i + 2]) == "11":
                ones_counter += 1
            if str(board[j][i]) + str(board[j + 1][i + 1]) + str(board[j + 2][i + 2]) == "22":
                twos_counter += 1
    for j in range(4):
        for i in range(2, 7):
            if str(board[j][i]) + str(board[j + 1][i - 1]) + str(board[j + 2][i - 2]) == "11":
                ones_counter += 1
            if str(board[j][i]) + str(board[j + 1][i - 1]) + str(board[j + 2][i - 2]) == "22":
                twos_counter += 1
    return [ones_counter, twos_counter]

def two_row(board):
    ones_counter = 0
    twos_counter = 0
    for j in range(6):
        for i in range(6):
            if str(board[j][i]) + str(board[j][i + 1]) == "11":
                ones_counter += 1
            if str(board[j][i]) + str(board[j][i + 1]) == "22":
                twos_counter += 1
    for j in range(5):
        for i in range(7):
            if str(board[j][i]) + str(board[j + 1][i]) == "11":
                ones_counter += 1
            if str(board[j][i]) + str(board[j + 1][i]) == "22":
                twos_counter += 1
    for j in range(5):
        for i in range(6):
            if str(board[j][i]) + str(board[j + 1][i + 1]) == "11":
                ones_counter += 1
            if str(board[j][i]) + str(board[j + 1][i + 1]) == "22":
                twos_counter += 1
    for j in range(5):
        for i in range(1, 7):
            if str(board[j][i]) + str(board[j + 1][i - 1]) == "11":
                ones_counter += 1
            if str(board[j][i]) + str(board[j + 1][i - 1]) == "22":
                twos_counter += 1
    return [ones_counter, twos_counter]

def evaluate(board):
    threes_1, threes_2 = three_row(board)
    twos_1, twos_2 = two_row(board)
    diff_threes = (threes_1 - threes_2) / 196
    diff_twos = (twos_1 - twos_2) / 262
    total_diff = max(-1, min(diff_threes + diff_twos, 1))
    return [total_diff, None]

def print_board(board):
    print("  1   2   3   4   5   6   7  ")
    print("-----------------------------")
    for r in board:
        print("| ", end="")
        for c in r:
            print((" " if c == 0 else "x" if c == 1 else "o" if c == 2 else c), end=" | ")
        print()
        print("-----------------------------")

def terminal(board):
    for j in range(6):
        for i in range(4):
            if str(board[j][i]) + str(board[j][i + 1]) + str(board[j][i + 2]) + str(board[j][i + 3]) == "1111":
                return [1, None]
            elif str(board[j][i]) + str(board[j][i + 1]) + str(board[j][i + 2]) + str(board[j][i + 3]) == "2222" :
                return [-1, None]
    for j in range(3):
        for i in range(7):
            if str(board[j][i]) + str(board[j + 1][i]) + str(board[j + 2][i]) + str(board[j + 3][i]) == "1111":
                return [1, None]
            elif str(board[j][i]) + str(board[j + 1][i]) + str(board[j + 2][i]) + str(board[j + 3][i]) == "2222":
                return [-1, None]
    for j in range(3):
        for i in range(4):
            if str(board[j][i]) + str(board[j + 1][i + 1]) + str(board[j + 2][i + 2]) + str(board[j + 3][i + 3]) == "1111":
                return [1, None]
            elif str(board[j][i]) + str(board[j + 1][i + 1]) + str(board[j + 2][i + 2]) + str(board[j + 3][i + 3]) == "2222":
                return [-1, None]
    for j in range(3):
        for i in range(3, 7):
            if str(board[j][i]) + str(board[j + 1][i - 1]) + str(board[j + 2][i - 2]) + str(board[j + 3][i - 3]) == "1111":
                return [1, None]
            elif str(board[j][i]) + str(board[j + 1][i - 1]) + str(board[j + 2][i - 2]) + str(board[j + 3][i - 3]) == "2222":
                return [-1, None]
    return None

def get_possible_moves(board):
    return [x for x in range(7) if [board[y][x] for y in range(6)].count(0) > 0]

def apply_move(board, turn, move):
    n = copy.deepcopy(board)
    for row in range(5, -1, -1):
        if n[row][move] == 0:
            n[row][move] = turn
            break
    return n

def minimax(board, is_max_turn, turn, curr_depth, max_depth, alpha=-float("inf"), beta=float("inf")):
    if curr_depth == max_depth:
        return evaluate(board)
    
    is_terminal = terminal(board)
    if is_terminal is not None:
        return is_terminal
    
    if is_max_turn:
        possible_moves = get_possible_moves(board)
        maximum_so_far = -float("inf")
        maximum_moves = []
        maximum_move = None
        for move in possible_moves:
            new_board = apply_move(board, turn, move)
            new_score = minimax(new_board, False, 3 - turn, curr_depth + 1, max_depth)
            if new_score[0] >= maximum_so_far:
                maximum_so_far = new_score[0]
                maximum_move = move
                maximum_moves.append([new_score, move])
            if maximum_so_far >= beta:
              break
            if maximum_so_far > alpha:
              alpha = maximum_so_far
        if curr_depth > 0:
            return [maximum_so_far, maximum_move]
        else:
            return maximum_moves
    else:
        possible_moves = get_possible_moves(board)
        minimum_so_far = float("inf")
        minimum_moves = []
        minimum_move = None
        for move in possible_moves:
            new_board = apply_move(board, turn, move)
            new_score = minimax(new_board, True, 3 - turn, curr_depth + 1, max_depth)
            if new_score[0] <= minimum_so_far:
                minimum_so_far = new_score[0]
                minimum_move = move
                minimum_moves.append([new_score, move])
            if minimum_so_far <= alpha:
              break
            if minimum_so_far < beta:
              beta = minimum_so_far
        if curr_depth > 0:
            return [minimum_so_far, minimum_move]
        else:
            return minimum_moves

def minimax_function(board, is_max_turn, turn, curr_depth, max_depth):
    original_is_max_turn = copy.copy(is_max_turn)
    possible_good_moves = minimax(board, is_max_turn, turn, curr_depth, max_depth)
    if original_is_max_turn:
        maximum_good_move = max(possible_good_moves, key=lambda l:l[0][0])[0][0]
        possible_good_moves = [possible_good_move for possible_good_move in possible_good_moves if possible_good_move[0][0] == maximum_good_move]
        nones = [possible_good_move1 for possible_good_move1 in possible_good_moves if possible_good_move1[0][1] is None]
        if len(nones) > 0:
            return random.choice(nones)[1]
        else:
            non_nones = [possible_good_move1 for possible_good_move1 in possible_good_moves if possible_good_move1[0][1] is not None]
            return random.choice(non_nones)[1]
    else:
        minimum_good_move = min(possible_good_moves, key=lambda l:l[0][0])[0][0]
        possible_good_moves = [possible_good_move for possible_good_move in possible_good_moves if possible_good_move[0][0] == minimum_good_move]
        nones = [possible_good_move1 for possible_good_move1 in possible_good_moves if possible_good_move1[0][1] is None]
        if len(nones) > 0:
            return random.choice(nones)[1]
        else:
            non_nones = [possible_good_move1 for possible_good_move1 in possible_good_moves if possible_good_move1[0][1] is not None]
            return random.choice(non_nones)[1]

pygame.init()
scr_width, scr_height = 720, 480
scr = pygame.display.set_mode((scr_width, scr_height))

while terminal(test_board) is None:
    print("Board:")
    print_board(test_board)
    test_board = apply_move(test_board, 1, int(input("\nEnter your move: ")) - 1)
    print("Board:")
    print_board(test_board)
    test_board = apply_move(test_board, 2, minimax_function(test_board, False, 2, 0, 5))
    print("\nComputer has played!\n")

print("Final Board:")
print_board(test_board)
result = terminal(test_board)[0]

print()
if result == 1:
    print("You won!")
else:
    print("The computer won!")
