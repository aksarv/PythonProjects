#importing all the necessary libraries
import pygame
import random
import socket
from Chessnut import Game
#connection to the server
'''HEADER = 64
PORT = 38747
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "10.1.129.149"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

#sending messages to the server
def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    print(client.recv(2048).decode(FORMAT))

'''

# COLOURS RGB
black = (0, 0, 0)
red = (255, 0, 0)
white = (255, 255, 255)
blue = (0, 0, 255)
cream = (255, 253, 208)
brown = (153, 77, 51)
dark = (77, 38, 25)
pygame.init()


# TEXT FUNCTION
def text(size, message, colour, x, y):
    font = pygame.font.SysFont(None, size)
    surface = font.render(message, True, colour)
    scr.blit(surface, (x, y))


# SCREEN
dimensions = (1024, 576)
scr = pygame.display.set_mode(dimensions)
pygame.display.set_caption('Chess')
# GAME LOOP
blackpawn = pygame.image.load(r'Re__code/Black Pawn.png')
blackknight = pygame.image.load(r'Re__code/Black Knight.png')
blackbishop = pygame.image.load(r'Re__code/Black Bishop.png')
blackrook = pygame.image.load(r'Re__code/Black Rook.png')
blackqueen = pygame.image.load(r'Re__code/Black Queen.png')
blackking = pygame.image.load(r'Re__code/Black King.png')
whitepawn = pygame.image.load(r'Re__code/White Pawn.png')
whiteknight = pygame.image.load(r'Re__code/White Knight.png')
whitebishop = pygame.image.load(r'Re__code/White Bishop.png')
whiterook = pygame.image.load(r'Re__code/White Rook.png')
whitequeen = pygame.image.load(r'Re__code/White Queen.png')
whiteking = pygame.image.load(r'Re__code/White King.png')

# BOUNCING PIECES SETUP
rand_list = []
pieces_on_screen = 10
for _ in range(pieces_on_screen):
    rand_x = random.randint(1, 824)
    rand_y = random.randint(1, 376)
    rand_size_mult = random.randint(1, 3)
    piece_choice = random.randint(1, 12)
    x_dir = random.choice([-1, 1])
    y_dir = random.choice([-1, 1])
    rand_list.append([rand_x, rand_y, piece_choice, rand_size_mult, x_dir, y_dir])

run = True
while run:
    # EVENT LOOP
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:  # IS THE MOUSE PRESSED
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if 410 < mouse_x < 610 and 350 < mouse_y < 415:
                playing = True
                while playing:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            quit()
                            send(DISCONNECT_MESSAGE)
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            m_x, m_y = pygame.mouse.get_pos()
                            if 410 < m_x < 610 and 350 < m_y < 415:  # online
                                scr = pygame.display.set_mode((1000, 800))
                                game = Game()
                                turn = 'White'
                                move = ''
                                computer = True
                                while computer:   #while loop for online chess
                                    for event in pygame.event.get():
                                        if event.type == pygame.QUIT:
                                            quit()
                                            send(DISCONNECT_MESSAGE)
                                        if event.type == pygame.KEYDOWN:
                                            if event.key == pygame.K_BACKSPACE:
                                                move = move[:-1]
                                            elif event.key == pygame.K_RETURN:
                                                if move in game.get_moves():
                                                    game.apply_move(move)
                                                    reply = send(f'PLAYMOVE  {str(game)}')
                                                    if reply != 'Move Sent' and reply is not None:
                                                        game.set_fen(reply)
                                                move = ''
                                            else:
                                                move += event.unicode
                                    scr.fill((255, 255, 255))
                                    colour = 'white'
                                    for x in range(8):  #drawing the chess board
                                        for y in range(9):
                                            if colour == 'white':
                                                pygame.draw.rect(scr, cream, [x * 100, y * 100, 100, 100])
                                                colour = 'black'
                                                continue
                                            if colour == 'black':
                                                pygame.draw.rect(scr, brown, [x * 100, y * 100, 100, 100])
                                                colour = 'white'
                                                continue
                                    text(40, 'Type move:', (0, 0, 0), 820, 40)
                                    text(40, move, (0, 0, 0), 840, 90)
                                    fen = str(game)
                                    fen = fen.split('/')
                                    fen[-1] = fen[-1].split(' ')[0]
                                    chessboard = []
                                    for x in fen:
                                        row = []
                                        for y in x:
                                            if y == '1' or y == '2' or y == '3' or y == '4' or y == '5' or y == '6' or y == '7' or y == '8' or y == '9':
                                                for z in range(int(y)):
                                                    row.append(' ')
                                            else:
                                                row.append(y)
                                        chessboard.append(row)
                                    for row in range(8):  #places the pieces on the board
                                        for col in range(8):
                                            square = chessboard[row][col]
                                            if square == 'p':
                                                scr.blit(blackpawn, (col * 100 + 20, row * 100 + 20))
                                            if square == 'n':
                                                scr.blit(blackknight, (col * 100 + 20, row * 100 + 20))
                                            if square == 'b':
                                                scr.blit(blackbishop, (col * 100 + 20, row * 100 + 20))
                                            if square == 'r':
                                                scr.blit(blackrook, (col * 100 + 20, row * 100 + 20))
                                            if square == 'q':
                                                scr.blit(blackqueen, (col * 100 + 20, row * 100 + 20))
                                            if square == 'k':
                                                scr.blit(blackking, (col * 100 + 20, row * 100 + 20))
                                            if square == 'P':
                                                scr.blit(whitepawn, (col * 100 + 20, row * 100 + 20))
                                            if square == 'N':
                                                scr.blit(whiteknight, (col * 100 + 20, row * 100 + 20))
                                            if square == 'B':
                                                scr.blit(whitebishop, (col * 100 + 20, row * 100 + 20))
                                            if square == 'R':
                                                scr.blit(whiterook, (col * 100 + 20, row * 100 + 20))
                                            if square == 'Q':
                                                scr.blit(whitequeen, (col * 100 + 20, row * 100 + 20))
                                            if square == 'K':
                                                scr.blit(whiteking, (col * 100 + 20, row * 100 + 20))
                                    pygame.display.update()
                            if 410 < m_x < 610 and 425 < m_y < 490:  # 2 player
                                scr = pygame.display.set_mode((1000, 800))
                                game = Game()
                                turn = 'White'
                                move = ''
                                computer = True
                                while computer:
                                    for event in pygame.event.get():
                                        if event.type == pygame.QUIT:
                                            quit()
                                            send(DISCONNECT_MESSAGE)
                                        if event.type == pygame.KEYDOWN:
                                            if event.key == pygame.K_BACKSPACE:
                                                move = move[:-1]
                                            elif event.key == pygame.K_RETURN:
                                                if move in game.get_moves():
                                                    game.apply_move(move)
                                                else:
                                                    incorrect_move_dialog = True
                                                move = ''
                                            else:
                                                move += event.unicode
                                    scr.fill((255, 255, 255))
                                    colour = 'white'
                                    for x in range(8):
                                        for y in range(9):
                                            if colour == 'white':
                                                pygame.draw.rect(scr, cream, [x * 100, y * 100, 100, 100])
                                                colour = 'black'
                                                continue
                                            if colour == 'black':
                                                pygame.draw.rect(scr, brown, [x * 100, y * 100, 100, 100])
                                                colour = 'white'
                                                continue
                                    text(40, 'Type move:', (0, 0, 0), 820, 40)
                                    text(40, move, (0, 0, 0), 840, 90)
                                    fen = str(game)
                                    fen = fen.split('/')
                                    fen[-1] = fen[-1].split(' ')[0]
                                    chessboard = []
                                    for x in fen:
                                        row = []
                                        for y in x:
                                            if y == '1' or y == '2' or y == '3' or y == '4' or y == '5' or y == '6' or y == '7' or y == '8' or y == '9':
                                                for z in range(int(y)):
                                                    row.append(' ')
                                            else:
                                                row.append(y)
                                        chessboard.append(row)
                                    for row in range(8):
                                        for col in range(8):
                                            square = chessboard[row][col]
                                            if square == 'p':
                                                scr.blit(blackpawn, (col * 100 + 20, row * 100 + 20))
                                            if square == 'n':
                                                scr.blit(blackknight, (col * 100 + 20, row * 100 + 20))
                                            if square == 'b':
                                                scr.blit(blackbishop, (col * 100 + 20, row * 100 + 20))
                                            if square == 'r':
                                                scr.blit(blackrook, (col * 100 + 20, row * 100 + 20))
                                            if square == 'q':
                                                scr.blit(blackqueen, (col * 100 + 20, row * 100 + 20))
                                            if square == 'k':
                                                scr.blit(blackking, (col * 100 + 20, row * 100 + 20))
                                            if square == 'P':
                                                scr.blit(whitepawn, (col * 100 + 20, row * 100 + 20))
                                            if square == 'N':
                                                scr.blit(whiteknight, (col * 100 + 20, row * 100 + 20))
                                            if square == 'B':
                                                scr.blit(whitebishop, (col * 100 + 20, row * 100 + 20))
                                            if square == 'R':
                                                scr.blit(whiterook, (col * 100 + 20, row * 100 + 20))
                                            if square == 'Q':
                                                scr.blit(whitequeen, (col * 100 + 20, row * 100 + 20))
                                            if square == 'K':
                                                scr.blit(whiteking, (col * 100 + 20, row * 100 + 20))
                                    text(20, 'a', (0, 0, 0), 10, 700)
                                    text(20, 'b', (0, 0, 0), 110, 700)
                                    text(20, 'c', (0, 0, 0), 210, 700)
                                    text(20, 'd', (0, 0, 0), 310, 700)
                                    text(20, 'e', (0, 0, 0), 410, 700)
                                    text(20, 'f', (0, 0, 0), 510, 700)
                                    text(20, 'g', (0, 0, 0), 610, 700)
                                    text(20, 'h', (0, 0, 0), 710, 700)
                                    text(20, '8', (0, 0, 0), 700, 10)
                                    text(20, '7', (0, 0, 0), 700, 110)
                                    text(20, '6', (0, 0, 0), 700, 210)
                                    text(20, '5', (0, 0, 0), 700, 310)
                                    text(20, '4', (0, 0, 0), 700, 410)
                                    text(20, '3', (0, 0, 0), 700, 510)
                                    text(20, '2', (0, 0, 0), 700, 610)
                                    text(20, '1', (0, 0, 0), 700, 710)
                                    pygame.display.update()

                            if 410 < m_x < 610 and 500 < m_y < 565:
                                # COMPUTER
                                scr = pygame.display.set_mode((1000, 800))
                                game = Game()
                                turn = 'White'
                                move = ''
                                incorrect_move_dialog = False
                                do_comp_move = False
                                computer = True
                                while computer:
                                    for event in pygame.event.get():
                                        if event.type == pygame.QUIT:
                                            quit()
                                            send(DISCONNECT_MESSAGE)
                                        if event.type == pygame.KEYDOWN:
                                            if event.key == pygame.K_BACKSPACE:
                                                move = move[:-1]
                                            elif event.key == pygame.K_RETURN:
                                                if move in game.get_moves():
                                                    game.apply_move(move)
                                                    do_comp_move = True
                                                else:
                                                    incorrect_move_dialog = True
                                                move = ''
                                            else:
                                                move += event.unicode
                                    scr.fill((255, 255, 255))
                                    colour = 'white'
                                    for x in range(8):
                                        for y in range(9):
                                            if colour == 'white':
                                                pygame.draw.rect(scr, cream, [x * 100, y * 100, 100, 100])
                                                colour = 'black'
                                                continue
                                            if colour == 'black':
                                                pygame.draw.rect(scr, brown, [x * 100, y * 100, 100, 100])
                                                colour = 'white'
                                                continue
                                    text(40, 'Type move:', (0, 0, 0), 820, 40)
                                    text(40, move, (0, 0, 0), 840, 90)
                                    if do_comp_move:
                                        game.apply_move(random.choice(game.get_moves()))
                                        do_comp_move = False
                                    fen = str(game)
                                    fen = fen.split('/')
                                    fen[-1] = fen[-1].split(' ')[0]
                                    chessboard = []
                                    for x in fen:
                                        row = []
                                        for y in x:
                                            if y == '1' or y == '2' or y == '3' or y == '4' or y == '5' or y == '6' or y == '7' or y == '8' or y == '9':
                                                for z in range(int(y)):
                                                    row.append(' ')
                                            else:
                                                row.append(y)
                                        chessboard.append(row)
                                    for row in range(8):
                                        for col in range(8):
                                            square = chessboard[row][col]
                                            if square == 'p':
                                                scr.blit(blackpawn, (col * 100 + 20, row * 100 + 20))
                                            if square == 'n':
                                                scr.blit(blackknight, (col * 100 + 20, row * 100 + 20))
                                            if square == 'b':
                                                scr.blit(blackbishop, (col * 100 + 20, row * 100 + 20))
                                            if square == 'r':
                                                scr.blit(blackrook, (col * 100 + 20, row * 100 + 20))
                                            if square == 'q':
                                                scr.blit(blackqueen, (col * 100 + 20, row * 100 + 20))
                                            if square == 'k':
                                                scr.blit(blackking, (col * 100 + 20, row * 100 + 20))
                                            if square == 'P':
                                                scr.blit(whitepawn, (col * 100 + 20, row * 100 + 20))
                                            if square == 'N':
                                                scr.blit(whiteknight, (col * 100 + 20, row * 100 + 20))
                                            if square == 'B':
                                                scr.blit(whitebishop, (col * 100 + 20, row * 100 + 20))
                                            if square == 'R':
                                                scr.blit(whiterook, (col * 100 + 20, row * 100 + 20))
                                            if square == 'Q':
                                                scr.blit(whitequeen, (col * 100 + 20, row * 100 + 20))
                                            if square == 'K':
                                                scr.blit(whiteking, (col * 100 + 20, row * 100 + 20))
                                    text(20, 'a', (0, 0, 0), 10, 700)
                                    text(20, 'b', (0, 0, 0), 110, 700)
                                    text(20, 'c', (0, 0, 0), 210, 700)
                                    text(20, 'd', (0, 0, 0), 310, 700)
                                    text(20, 'e', (0, 0, 0), 410, 700)
                                    text(20, 'f', (0, 0, 0), 510, 700)
                                    text(20, 'g', (0, 0, 0), 610, 700)
                                    text(20, 'h', (0, 0, 0), 710, 700)
                                    text(20, '8', (0, 0, 0), 700, 10)
                                    text(20, '7', (0, 0, 0), 700, 110)
                                    text(20, '6', (0, 0, 0), 700, 210)
                                    text(20, '5', (0, 0, 0), 700, 310)
                                    text(20, '4', (0, 0, 0), 700, 410)
                                    text(20, '3', (0, 0, 0), 700, 510)
                                    text(20, '2', (0, 0, 0), 700, 610)
                                    text(20, '1', (0, 0, 0), 700, 710)
                                    pygame.display.update()
                    scr.fill(cream)
                    text(100, 'Choose how to play', dark, 350, 40)
                    pygame.draw.rect(scr, brown, [410, 350, 200, 65])
                    pygame.draw.rect(scr, brown, [410, 425, 200, 65])
                    pygame.draw.rect(scr, brown, [410, 500, 200, 65])
                    text(40, 'Online', cream, 470, 360)
                    text(40, '2 Player', cream, 430, 435)
                    text(40, 'vs Computer', cream, 430, 510)
                    for piece in rand_list:
                        x_pos = piece[0]
                        y_pos = piece[1]
                        choice = piece[2]
                        size_mult = piece[3]
                        if x_pos >= 874 or x_pos <= 0:
                            piece[4] *= -1
                        if y_pos >= 426 or y_pos <= 0:
                            piece[5] *= -1
                        if choice == 1:     #sets the sizes of the pieces
                            Piece = pygame.transform.scale(blackpawn, (60 * size_mult, 60 * size_mult))
                            scr.blit(Piece, (x_pos, y_pos))
                            piece[0] += piece[4]
                            piece[1] += piece[5]
                        if choice == 2:
                            Piece = pygame.transform.scale(blackknight, (60 * size_mult, 60 * size_mult))
                            scr.blit(Piece, (x_pos, y_pos))
                            piece[0] += piece[4]
                            piece[1] += piece[5]
                        if choice == 3:
                            Piece = pygame.transform.scale(blackbishop, (60 * size_mult, 60 * size_mult))
                            scr.blit(Piece, (x_pos, y_pos))
                            piece[0] += piece[4]
                            piece[1] += piece[5]
                        if choice == 4:
                            Piece = pygame.transform.scale(blackrook, (60 * size_mult, 60 * size_mult))
                            scr.blit(Piece, (x_pos, y_pos))
                            piece[0] += piece[4]
                            piece[1] += piece[5]
                        if choice == 5:
                            Piece = pygame.transform.scale(blackqueen, (60 * size_mult, 60 * size_mult))
                            scr.blit(Piece, (x_pos, y_pos))
                            piece[0] += piece[4]
                            piece[1] += piece[5]
                        if choice == 6:
                            Piece = pygame.transform.scale(blackking, (60 * size_mult, 60 * size_mult))
                            scr.blit(Piece, (x_pos, y_pos))
                            piece[0] += piece[4]
                            piece[1] += piece[5]
                        if choice == 7:
                            Piece = pygame.transform.scale(whitepawn, (60 * size_mult, 60 * size_mult))
                            scr.blit(Piece, (x_pos, y_pos))
                            piece[0] += piece[4]
                            piece[1] += piece[5]
                        if choice == 8:
                            Piece = pygame.transform.scale(whiteknight, (60 * size_mult, 60 * size_mult))
                            scr.blit(Piece, (x_pos, y_pos))
                            piece[0] += piece[4]
                            piece[1] += piece[5]
                        if choice == 9:
                            Piece = pygame.transform.scale(whitebishop, (60 * size_mult, 60 * size_mult))
                            scr.blit(Piece, (x_pos, y_pos))
                            piece[0] += piece[4]
                            piece[1] += piece[5]
                        if choice == 10:
                            Piece = pygame.transform.scale(whiterook, (60 * size_mult, 60 * size_mult))
                            scr.blit(Piece, (x_pos, y_pos))
                            piece[0] += piece[4]
                            piece[1] += piece[5]
                        if choice == 11:
                            Piece = pygame.transform.scale(whitequeen, (60 * size_mult, 60 * size_mult))
                            scr.blit(Piece, (x_pos, y_pos))
                            piece[0] += piece[4]
                            piece[1] += piece[5]
                        if choice == 12:
                            Piece = pygame.transform.scale(whiteking, (60 * size_mult, 60 * size_mult))
                            scr.blit(Piece, (x_pos, y_pos))
                            piece[0] += piece[4]
                            piece[1] += piece[5]
                    pygame.display.update()
            if 410 < mouse_x < 610 and 425 < mouse_y < 490:
                howtoplay = True
                while howtoplay:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            howtoplay = False
                    scr.fill(cream)
                    text(40, "How to Play the game:", dark, 405, 160)
                    text(30, "To move, you type in the piece, the current position of the piece, and the square you want to move it to.", dark, 20, 210)
                    text(30, "E.g., if white's pawn is on e2, to move it to e4 you would type e2e4.", dark, 20, 260)



                    pygame.display.update()
    scr.fill(cream)
    for piece in rand_list:
        x_pos = piece[0]
        y_pos = piece[1]
        choice = piece[2]
        size_mult = piece[3]
        if x_pos >= 874 or x_pos <= 0:
            piece[4] *= -1
        if y_pos >= 426 or y_pos <= 0:
            piece[5] *= -1
        if choice == 1:
            Piece = pygame.transform.scale(blackpawn, (60 * size_mult, 60 * size_mult))
            scr.blit(Piece, (x_pos, y_pos))
            piece[0] += piece[4]
            piece[1] += piece[5]
        if choice == 2:
            Piece = pygame.transform.scale(blackknight, (60 * size_mult, 60 * size_mult))
            scr.blit(Piece, (x_pos, y_pos))
            piece[0] += piece[4]
            piece[1] += piece[5]
        if choice == 3:
            Piece = pygame.transform.scale(blackbishop, (60 * size_mult, 60 * size_mult))
            scr.blit(Piece, (x_pos, y_pos))
            piece[0] += piece[4]
            piece[1] += piece[5]
        if choice == 4:
            Piece = pygame.transform.scale(blackrook, (60 * size_mult, 60 * size_mult))
            scr.blit(Piece, (x_pos, y_pos))
            piece[0] += piece[4]
            piece[1] += piece[5]
        if choice == 5:
            Piece = pygame.transform.scale(blackqueen, (60 * size_mult, 60 * size_mult))
            scr.blit(Piece, (x_pos, y_pos))
            piece[0] += piece[4]
            piece[1] += piece[5]
        if choice == 6:
            Piece = pygame.transform.scale(blackking, (60 * size_mult, 60 * size_mult))
            scr.blit(Piece, (x_pos, y_pos))
            piece[0] += piece[4]
            piece[1] += piece[5]
        if choice == 7:
            Piece = pygame.transform.scale(whitepawn, (60 * size_mult, 60 * size_mult))
            scr.blit(Piece, (x_pos, y_pos))
            piece[0] += piece[4]
            piece[1] += piece[5]
        if choice == 8:
            Piece = pygame.transform.scale(whiteknight, (60 * size_mult, 60 * size_mult))
            scr.blit(Piece, (x_pos, y_pos))
            piece[0] += piece[4]
            piece[1] += piece[5]
        if choice == 9:
            Piece = pygame.transform.scale(whitebishop, (60 * size_mult, 60 * size_mult))
            scr.blit(Piece, (x_pos, y_pos))
            piece[0] += piece[4]
            piece[1] += piece[5]
        if choice == 10:
            Piece = pygame.transform.scale(whiterook, (60 * size_mult, 60 * size_mult))
            scr.blit(Piece, (x_pos, y_pos))
            piece[0] += piece[4]
            piece[1] += piece[5]
        if choice == 11:
            Piece = pygame.transform.scale(whitequeen, (60 * size_mult, 60 * size_mult))
            scr.blit(Piece, (x_pos, y_pos))
            piece[0] += piece[4]
            piece[1] += piece[5]
        if choice == 12:
            Piece = pygame.transform.scale(whiteking, (60 * size_mult, 60 * size_mult))
            scr.blit(Piece, (x_pos, y_pos))
            piece[0] += piece[4]
            piece[1] += piece[5]
    text(100, 'Chess', dark, 405, 40)  #home screen title
    pygame.draw.rect(scr, dark, [410, 350, 200, 65])
    pygame.draw.rect(scr, dark, [410, 425, 200, 65])
    text(40, 'Guest', cream, 470, 360) #option to play as guest
    text(40, 'How to play', cream, 430, 435) #option to see how to play

    pygame.display.update()

pygame.quit()
send(DISCONNECT_MESSAGE)

