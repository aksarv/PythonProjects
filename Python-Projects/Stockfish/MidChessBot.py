# Plays median move every time in terms of evaluation. Allows a complete game to be played and the PGN to be saved
import chess
import chess.engine
import chess.pgn
import random
import pygame
import copy
import datetime

pygame.init()
scr_width, scr_height = 720, 480
scr = pygame.display.set_mode((scr_width, scr_height))
pygame.display.set_caption("Mid Chess Bot")

board_width = 480
board_height = 480
start_board_x = scr_width//2 - board_width//2
start_board_y = scr_height//2 - board_height//2

stockfish_path = "/opt/homebrew/bin/stockfish"

board = chess.Board()

with chess.engine.SimpleEngine.popen_uci(stockfish_path) as engine:
    board.set_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    pgn_game = chess.pgn.Game()
    node = pgn_game.add_variation(board.san(chess.Move.null()))
    # To find median move rank all legal moves by evaluation then pick the median from the list
    run = True
    while not board.is_game_over() and run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        scr.fill((0, 0, 0))
        moves = []
        for move in board.legal_moves:
            board.push(move)
            evaluation = engine.analyse(board, chess.engine.Limit(time=0.2))["score"]
            if evaluation is not None:
                moves.append((move, evaluation))
            board.pop()
        moves = sorted(moves, key=lambda l:l[1].relative.score() if l[1].relative.score() is not None else 0, reverse=True)
        if len(moves) % 2 == 0:
            median_move = random.choice([moves[len(moves)//2-1], moves[len(moves)//2]])
        else:
            median_move = moves[len(moves)//2]
        scr.blit(pygame.font.SysFont('Arial', 12).render(f"{('White' if board.turn else 'Black')} played {board.san(chess.Move.from_uci(str(median_move[0])))}.", True, (255, 255, 255)), (15, 15))
        board.push(chess.Move.from_uci(str(median_move[0])))
        node = node.add_variation(move)
        board_state = board.fen().split("/")[:-1] + [board.fen().split("/")[-1].split(" ")[0]]
        for a in range(8):
            for b in range(8):
                if (a + b) % 2 == 1:
                    pygame.draw.rect(scr, (101, 67, 33), [b * (board_width // 8) + start_board_x, a * (board_height // 8) + start_board_y, board_width // 8, board_height // 8])
                else:
                    pygame.draw.rect(scr, (255, 255, 255), [b * (board_width // 8) + start_board_x, a * (board_height // 8) + start_board_y, board_width // 8, board_height // 8])
        for i, r in enumerate(board_state):
            offset = 0
            for j, c in enumerate(r):
                char = c
                if char.isnumeric():
                    offset += int(c)
                else:
                    file_name = f"{('Black' if char.islower() else 'White')} {'Pawn' if char.lower() == 'p' else 'Knight' if char.lower() == 'n' else 'King' if char.lower() == 'k' else 'Bishop' if char.lower() == 'b' else 'Rook' if char.lower() == 'r' else 'Queen' if char.lower() == 'q' else ''}.png"
                    scr.blit(pygame.transform.scale(pygame.image.load(file_name), (board_width // 8, board_height // 8)), (offset * (board_width // 8) + start_board_x, i * (board_height // 8) + start_board_y))
                    offset += 1
        pygame.display.update()
    if board.is_checkmate():
        cause = "Game ended due to checkmate."
    elif board.is_stalemate():
        cause = "Game ended due to stalemate."
    elif board.is_insufficient_material():
        cause = "Game ended due to insufficient material."
    elif board.is_fifty_moves():
        cause = "Game ended due to 50-move rule."
    elif board.is_variant_draw():
        cause = "Game ended due to draw by threefold repetition or another variant draw."
    else:
        cause = "Game ended for an unknown reason."
    node.comment = "{" + cause + "}"
    with open(f"Game{datetime.datetime.now().strftime('%y-%m-%d-%H-%M-%S')}.pgn", "w") as game_file:
        print(pgn_game, file=game_file)
        print("Game written successfully!")
