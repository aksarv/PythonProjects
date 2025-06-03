import math
import random
import threading
import socket

# Bytes of data to receive or send
header_length = 8192
format = 'utf-8'

# Storing the port the server will run on; typically 5050 or 8000 is
# available
port = 5050

# Finds the local IP to run the server on
ip = socket.gethostbyname(socket.gethostname())

# Creating a socket.socket object to represent the server and allow
# it to interact with clients
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Adding the IP and port to run the server on
server.bind((ip, port))

class Player:
    # Setting the initial attributes of the player class
    def __init__(self, conn, username, colour):
        # This stores the player's x and y coordinates
        # Player should spawn in a random x and y position
        # that does not exceed the window dimensions
        self.x = random.randint(0, 2300)
        self.y = random.randint(0, 1294)

        # Stores the username of the player
        self.username = username

        # Stores the socket.socket object representing the
        # player in string format to uniquely distinguish
        # that player
        self.id = conn

        # Stores the player's colour
        self.colour = colour

        # Stores the player's XP
        self.xp = 1

class Arena:
    # Setting the initial attributes of the arena class
    def __init__(self):
        # This will store Player objects representing the
        # players who are in the arena
        self.players = []

        self.leaderboard = []

        # This stores the maximum number of players who can
        # join an arena; if the number of players in an
        # arena is equal to its capacity, the next arena
        # will be tested. If all arenas are full, a new
        # arena is created to add the player to
        self.capacity = 10

        # Stores a 2D array consisting of the username
        # and the message sent
        self.chat = []

        # This will store Pellet objects representing the
        # pellets in the arena that players will eat
        self.pellets = [Pellet() for _ in range(100)]

class Pellet:
    # Setting the initial attributes of the pellet class
    def __init__(self):
        # This stores the pellet's x and y coordinates
        # Pellet should spawn in a random x and y position
        # that does not exceed the screen dimensions
        self.x = random.randint(0, 2300)
        self.y = random.randint(0, 1294)

        # This stores the pellet's colour
        # It should be a random choice between a selection
        # of red, yellow, green and blue
        self.colour = random.choice([(255, 0, 0), (0, 255, 0),
                                     (0, 0, 255), (252, 238, 124)])
        
        # Stores the unique ID of each pellet so it can be
        # identified later during collision detection between
        # the player and the pellet
        self.id = random.randint(10000, 99999)

# Initialising a list to store all of the arenas; when the
# server is created, one arena should already be ready
arenas = [Arena()]

def handle_client(conn, addr):
    connected = True
    while connected:
        # The following line of code blocks the server code until the client sends a message to the server
        msg_length = conn.recv(header_length).decode(format)

        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(format)
            if msg == 'LEAVE':
                # Client wants to leave - finding which arena's list of players to remove them from
                for a, arena in enumerate(arenas):
                    for b, player in enumerate(arena.players):
                            if f'{arenas[a].players[b].id}' == f'{conn}':
                                del arenas[a].players[b]
                connected = False
            if msg.startswith('MOVE'):
                
                x_vel, y_vel = eval(msg.split(' ')[1]), eval(msg.split(' ')[2])
                for i, arena in enumerate(arenas):
                    breakout = False
                    for j, player in enumerate(arena.players):
                        if f'{player.id}' == f'{conn}':
                            arenas[i].players[j].x += x_vel
                            arenas[i].players[j].y += y_vel
                            breakout = True
                            break
                    if breakout:
                        break
            if msg.startswith('USERNAME'):
                # Client is sending their username and wants to join an arena
                username = msg.split(' ')[1]
                for i, arena in enumerate(arenas):
                    if len(arena.players) < arena.capacity:
                        arenas[i].players.append(Player(conn, username, (random.randint(0, 255), 
                                                                         random.randint(0, 255), random.randint(0, 255))))
                        break
                else:
                    # If no arenas have space, create a new arena and add the client to it
                    arenas.append(Arena())
                    arenas[-1].players.append(Player(conn, username, (random.randint(0, 255), 
                                                                      random.randint(0, 255), random.randint(0, 255))))
            if msg.startswith('COLLISION'):
                print('client reported collision')
                # Client reporting a collision between two players
                split = msg.split('  ')
                xp, xp2, id, id2 = eval(split[1]), eval(split[2]), split[3], split[4]
                print(xp, xp2, id, id2)
                for i, arena in enumerate(arenas):
                    for j, player in enumerate(arena.players):
                        if f'{player.id}' == id:
                            for k, player2 in enumerate(arena.players):
                                if f'{player2.id}' == id2:
                                    if xp > xp2:
                                        arenas[i].players[j].xp += arenas[i].players[k].xp
                                        arenas[i].players[k].xp = 1
                                        arenas[i].players[k].x = random.randint(0, 2300)
                                        arenas[i].players[k].y = random.randint(0, 1294)
                                    elif xp2 > xp:
                                        arenas[i].players[k].xp += arenas[i].players[j].xp
                                        arenas[i].players[j].xp = 1
                                        arenas[i].players[j].x = random.randint(0, 2300)
                                        arenas[i].players[j].y = random.randint(0, 1294)
                                        
            if msg.startswith('PELLET'):
                split = msg.split('  ')
                xp, id2, id = split[1], split[2], split[3]
                for i, arena in enumerate(arenas):
                    for j, player in enumerate(arena.players):
                        if f'{player.id}' == id2:
                            for k, pellet in enumerate(arena.pellets):
                                if f'{pellet.id}' == id:
                                    arenas[i].pellets[k].x = random.randint(0, 2300)
                                    arenas[i].pellets[k].y = random.randint(0, 1294)
                                    arenas[i].pellets[k].colour = random.choice([(255, 0, 0), (255, 128, 0), (0, 255, 255), (0, 255, 0), (0, 128, 128), (0, 0, 255)])
                                    arenas[i].players[j].xp += 0.5
            
            if msg.startswith('CHAT'):
                split = msg.split('  ')
                id, chat_message = split[1], split[2]
                for i, arena in enumerate(arenas):
                    for j, player in enumerate(arena.players):
                        if f'{player.id}' == id:
                            arenas[i].chat.append([player.username, chat_message])
                            

        for arena in arenas:
            breakout = False
            for player in arena.players:
                if f'{player.id}' == f'{conn}':
                    # The attributes of the player class are being converted into list form so they can be sent
                    # in text format to be evaluated and read easily in the client code
                    player_datas = []
                    for p in arena.players:
                        data = [p.x, p.y, p.username, p.colour, p.xp, f'{p.id}']
                        player_datas.append(data)
                    pellets_list = []
                    for pellet in arena.pellets:
                        pellets_list.append([pellet.x, pellet.y, pellet.colour, pellet.id])
                    breakout = True
                    break
            if breakout:
                break
        # Sending all the data the server has stored to each client.
        conn.sendall(f'{player_datas};{arena.chat};{arena.leaderboard} \
                     ;{player.x};{player.y};{pellets_list};{player.xp}; \
                     {player.id}'.encode(format))
    # The following line of code is only reached once variable "connected" is False, when the player leaves the game
    conn.close()

# Detect any incoming requests to join the server
server.listen()
# IP and port details are to be copied to the respective variables in 
# the client code to make a connection, hence printed here
print(f"Server is running on IP {ip} under port {port}")
while True:
    # The following line of code blocks the program until a connection 
    # is made when a client has requested to join the server
    # It captures the objects needed to communicate with the client
    conn, addr = server.accept()
    # The variable "conn" is the socket.socket object that is used to
    # send messages to/receive messages from the client, as it has 
    # functions to do this
    
    # Starting a separate asynchronous thread to handle each client in
    # parallel; "conn" is passed as an argument
    # This function - "handle_client()" - is run in parallel for each 
    # client so sending messages to/receiving messages from all clients
    # is done simultaneously
    thread = threading.Thread(target=handle_client, args=(conn, addr))
    thread.start()
