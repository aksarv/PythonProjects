import time
import math
import pygame
import socket

pygame.init()

# Function that renders any text, including centred text
def text(size, message, color, xpos, ypos, centre_x=None, centre_y=None):
    if centre_x == None and centre_y == None:
        scr.blit(pygame.font.SysFont('Tahoma', size).render(message, True, 
                                                            color), (xpos, ypos))
    else:
        scr.blit(pygame.font.SysFont('Tahoma', size).render(message, True, color), 
                 pygame.font.SysFont('Tahoma', size).render(message, True, color)
                 .get_rect(center=(centre_x, centre_y)))

fps = 120

scr_width, scr_height = 2300, 1294

scr = pygame.display.set_mode((scr_width, scr_height))

clock = pygame.time.Clock()

run1 = True

message = ''

while run1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run1 = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                message = message[:-1]
            elif event.key == pygame.K_RETURN:
                run1 = False
            else:
                message += event.unicode

    scr.fill((0, 0, 0))
    text(50, 'Enter server IP here: ' + message, (255, 255, 255), 0, 0, centre_x=scr_width//2, centre_y=scr_height//2)
    pygame.display.update()
    clock.tick(fps)

run2 = True

message1 = ''

while run2:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run2 = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                message1 = message1[:-1]
            elif event.key == pygame.K_RETURN:
                run2 = False
            else:
                message1 += event.unicode

    scr.fill((0, 0, 0))
    text(50, 'Enter server port here: ' + message1, (255, 255, 255), 0, 0, centre_x=scr_width//2, centre_y=scr_height//2)
    pygame.display.update()
    clock.tick(fps)

# Bytes of data to receive or send
header = 8192
format = 'utf-8'

# The port the server will run on; this will be copied from the server code
port = 5050
# The first value in the address will be the local IP the server is running
# on, which is also copied from the server code
address = (message, int(message1))

# Initialising a socket.socket object to represent the client and allow it
# to interact with the server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Establishing a connection by connecting the client to the server's address
client.connect(address)

# This function sends data to and returns the response from the server
def send(msg):
    # Encoding the message; must be done to send it
    message = msg.encode(format)
    # Creating a message to send the server so it knows
    # how much bytes to expect to read
    msg_length = len(message)
    send_length = str(msg_length).encode(format)
    send_length += b' ' * (header - len(send_length))
    # Sending the length of the message first so the
    # server knows how much bytes to expect to read
    client.send(send_length)
    # Sending the encoded message
    client.send(message)
    # Returning the response from the server
    return str(client.recv(8192).decode(format))

def leave_game():
    scr.fill((0, 0, 0))
    text(100, 'Bye!', (255, 0, 0), 0, 0, centre_x=scr_width//2, centre_y=scr_height//2)
    pygame.display.update()
    time.sleep(5)
    send("LEAVE")
    pygame.quit()
    quit()

def wrap_text(text, chars):
    return [list(text[x:x+chars]) for x in range(0, len(text), chars)]

username = ''

entered_username = False
run = True
while run:    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if not entered_username:
                if event.key == pygame.K_RETURN:
                    entered_username = True
                    send(f"USERNAME {username}")
                elif event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                else:
                    username += event.unicode


    scr.fill((0, 0, 0))

    # The following code is run if the user has not entered their username yet (this is needed to be added to the
    # server and an arena as it is a parameter that must be provided to the __init__ function of the Player class)
    if not entered_username:
        text(50, 'What would you like to be called?', (255, 255, 255), 0, 0, centre_x=scr_width//2, centre_y=100)
        text(20, 'Type a username below.', (255, 255, 255), 0, 0, centre_x=scr_width//2, centre_y=200)
        text(20, 'Then, press Enter to play.', (255, 255, 255), 0, 0, centre_x=scr_width//2, centre_y=250)
        text(30, username, (255, 255, 255), 0, 0, centre_x=scr_width//2, centre_y=scr_height//2)
    # Once the user has entered their username, only the following code will run
    else:
        # Making player_x and player_y global variables (accessible in any scope) such that the code
        # for moving the player towards the mouse can access them
        global player_x
        global player_y
        global player_id
        chat_message = ''
        run2 = True
        clock2 = pygame.time.Clock()
        while run2:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    leave_game()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        send(f"CHAT  {player_id}  {chat_message}")
                        chat_message = ''
                    elif event.key == pygame.K_BACKSPACE:
                        chat_message = chat_message[:-1]
                    else:
                        chat_message += event.unicode

            scr.fill((0, 0, 0))

            scene = send("INFO")
            # First level of testing - printing the entire, unprocessed
            # message sent by the server
            print(scene)
            # Splitting the different values by the semicolon delimiter
            arena = scene.split(';')
            # Second level of testing - checking that the first part
            # of processing - splitting it by the intentional delimiter
            # added in the server code - was valid.
            print(arena)
            # Quitting immediately to examine the data.


            # Unpacking the data about the arena sent by the server to display it for the client
            players, chat, leaderboard, player_x, player_y, pellets, player_xp, player_id = arena
            player_x = float(player_x)
            player_y = float(player_y)
            # Evaluating each input to convert it from a string into a list so its values can be
            # easily accessed and displayed
            players, chat, leaderboard, pellets = eval(players), eval(chat), eval(leaderboard), eval(pellets)

            for pellet in pellets:
                x, y, colour, id = pellet
                pygame.draw.circle(scr, colour, (x, y), 5)
                for player in players:
                    x2, y2, _, _, xp, id2 = player
                    distance_between_circles = math.sqrt((y2-y)**2+(x2-x)**2)
                    if distance_between_circles < xp*2+20 or distance_between_circles < 5:
                        send(f"PELLET  {xp}  {id2}  {id}")

            for player in players:
                x, y, username, colour, xp, id = player
                # Drawing a circle for each player as part of displaying the game
                pygame.draw.circle(scr, colour, (x, y), xp*2+20)
                text(int((xp*2+20)/2), username, (255, 255, 255), 0, 0, centre_x=x, centre_y=y)
                # Iterating through the players again to check any two players
                for player2 in players:
                    x2, y2, _, _, xp2, id2 = player2
                    # The following is done to prevent the same player from being chosen twice
                    if x != x2 and y != y2:
                        # If the distance between the circles is smaller than either of the circles'
                        # radii, the player is considered 'consumed'
                        distance_between_circles = math.sqrt((y2-y)**2+(x2-x)**2)
                        if distance_between_circles < xp*2+20 or distance_between_circles < xp2*2+20:
                            # Telling the server that there was a collision
                            send(f"COLLISION  {xp}  {xp2}  {id}  {id2}")

            players_and_scores = []
            for player in players:
                _, _, username, _, xp, _ = player
                players_and_scores.append([username, xp])

            text(40, 'Leaderboard', (255, 255, 255), 0, 0, centre_x=2175, centre_y=25)
            leaderboard = sorted(players_and_scores, key=lambda l:l[1])[::-1]
            for i, l in enumerate(leaderboard):
                text(20, f'{i+1}. {l[0]} ({l[1]} XP)', (255, 255, 255), 2067, i*20+65)
                if i == 4:
                    break

            text(40, 'Chat Room', (255, 255, 255), 0, 0, centre_x=2175, centre_y=550)
            wrapped_preview = wrap_text(chat_message, 20)
            for j, line in enumerate(wrapped_preview):
                text(20, ''.join(line), (255, 255, 255), 2067, 600+j*25)

            last_5_messages = chat[-5:]
            for i, message in enumerate(last_5_messages):
                wrapped_message = wrap_text(f'{message[0]}: ' + message[1], 20)
                
                for j, line in enumerate(wrapped_message):
                    text(20, ''.join(line), (255, 255, 255), 2067, i*100+650+j*25)
            
            # The player's overall speed should always be a set value, depending on their size, regardless of the
            # direction the mouse is. To do this, the hypotenuse of a right-angled triangle between the player's 
            # and the mouse's positions should always be this overall speed.
            # Once the smaller sides are used to calculate the actual hypotenuse, this can be scaled down to the
            # overall speed we desire, and its x and y components can be calculated and sent to the server, so that
            # the server knows how to move the player.

            x2, y2 = pygame.mouse.get_pos()
            x1, y1 = player_x, player_y
            
            # First, the shorter sides of the non-scaled right-angled triangle should be calculated by finding the
            # difference between the x positions and the difference between the y positions.
            delta_y = y2-y1
            delta_x = x2-x1

            # Then, the hypotenuse of the non-scaled right angled triangle should be calculated
            # The absolute value is used to prevent two differently signed shorter side lengths cancelling out
            hypotenuse = math.sqrt(abs(delta_x)**2+abs(delta_y)**2)
            
            # The reciprocal function y=7/x is used to calculate the player's speed such that the player moves
            # slower the larger they get
            scale_factor = (7 / float(player_xp)) / hypotenuse
            new_delta_x = delta_x * scale_factor
            new_delta_y = delta_y * scale_factor

            # Sending the x and y components to the server so it can update the player's position
            send(f"MOVE {new_delta_x} {new_delta_y}")

            pygame.display.update()
            clock2.tick(fps)

    clock.tick(fps)
    pygame.display.update()

pygame.quit()