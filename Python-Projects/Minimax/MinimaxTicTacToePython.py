import copy
import itertools


def pretty_print_2d_list(two_d_list):
  for row in two_d_list:
    row_string = ""
    for col in row:
      row_string += str(col) + " "
    print(row_string)


def get_next_states(current_state, turn):
  for i, r in enumerate(current_state):
    for j, c in enumerate(r):
      if c == " ":
        current_state_copy = copy.deepcopy(current_state)
        current_state_copy[i][j] = turn
        yield current_state_copy


def get_evaluation_of_terminal(game_state, turn):
  if (game_state[0][0] == "X" and game_state[0][1] == "X"
      and game_state[0][2] == "X") or (
          game_state[1][0] == "X" and game_state[1][1] == "X"
          and game_state[1][2] == "X") or (
              game_state[2][0] == "X" and game_state[2][1] == "X"
              and game_state[2][2] == "X") or (
                  game_state[0][0] == "X"
                  and game_state[1][0] == "X" and game_state[2][0] == "X") or (
                      game_state[0][1] == "X" and game_state[1][1] == "X"
                      and game_state[2][1] == "X") or (
                          game_state[0][2] == "X" and game_state[1][2] == "X"
                          and game_state[2][2] == "X") or (
                              game_state[0][0] == "X"
                              and game_state[1][1] == "X" and game_state[2][2]
                              == "X") or (game_state[2][0] == "X"
                                          and game_state[1][1] == "X"
                                          and game_state[0][2] == "X"):
    if turn == "O":
      return 1
    else:
      return -1
  elif (game_state[0][0] == "O" and game_state[0][1] == "O"
        and game_state[0][2] == "O") or (
            game_state[1][0] == "O" and game_state[1][1] == "O"
            and game_state[1][2] == "O"
        ) or (game_state[2][0] == "O" and game_state[2][1] == "O"
              and game_state[2][2] == "O") or (
                  game_state[0][0] == "O" and game_state[1][0] == "O"
                  and game_state[2][0] == "O") or (
                      game_state[0][1] == "O" and game_state[1][1] == "O"
                      and game_state[2][1] == "O") or (
                          game_state[0][2] == "O" and game_state[1][2] == "O"
                          and game_state[2][2] == "O") or (
                              game_state[0][0] == "O"
                              and game_state[1][1] == "O" and game_state[2][2]
                              == "O") or (game_state[2][0] == "O"
                                          and game_state[1][1] == "O"
                                          and game_state[0][2] == "O"):
    if turn == "X":
      return 1
    else:
      return -1
  elif list(itertools.chain.from_iterable(game_state)).count(" ") == 0:
    return 0
  else:
    return "Not Finished"


def minimax(current_state, turn, is_max=True, current_depth=1):
  evaluation = get_evaluation_of_terminal(current_state, turn)
  print("Current State:")
  pretty_print_2d_list(current_state)
  print(f"Current Depth: {current_depth}")
  if evaluation != "Not Finished":
    print("Current state IS a terminal node")
    print(f"Evaluation of Terminal Node: {evaluation}")
    return evaluation
  else:
    print("Current state is NOT a terminal node")
    if is_max:
      print("is_max=" + str(is_max))
      maximum = -float("inf")
      for next_states in get_next_states(current_state, turn):
        if minimax(next_states, ("X" if turn == "O" else "O"),
                   is_max=False,
                   current_depth=current_depth + 1) >= maximum:
          maximum = minimax(next_states, ("X" if turn == "O" else "O"),
                            is_max=False,
                            current_depth=current_depth + 1)
      return maximum
    else:
      minimum = float("inf")
      for next_states in get_next_states(current_state, turn):
        if minimax(next_states, ("X" if turn == "O" else "O"),
                   is_max=True,
                   current_depth=current_depth + 1) <= minimum:
          minimum = minimax(next_states, ("X" if turn == "O" else "O"),
                            is_max=True,
                            current_depth=current_depth + 1)
      return minimum


print(minimax([["X", "O", "X"], ["O", " ", " "], [" ", " ", " "]], "X"))
