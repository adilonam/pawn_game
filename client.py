# import the socket module
import pygame
from board import ChessBoard
from UserInterface import UserInterface
import socket

global time
global color
global surface
global UI

# Create a socket instance

socketObject = socket.socket()

# Using the socket connect to a server...in this case localhost

socketObject.connect(("localhost",9999))

# Initialize game mode
game_mode = "player_vs_player"  # Default mode

# Send a message to the web server to supply a page as given by Host param of GET request

while (True):

    data = socketObject.recv(1024)
    data = data.decode()

    print(data)

    if data.startswith("Time"):
        time = int(data[4:]) * 60 # Convert minutes to seconds
        msg = "OK"
        msg = msg.encode()
        socketObject.send(msg)
# Setup Wb4 Wa3 Wc2 Bg7 Wd4 Bg6 Be7
    elif data.startswith("Setup"):
        time = 900
        pygame.init()  # initialize pygame
        surface = pygame.display.set_mode([600, 600], 0, 0)
        pygame.display.set_caption('Pawn Game')
        Board = ChessBoard()
        UI = UserInterface(surface, Board)
        pawn_num = 0
        UI.firstgame = False
        for i in range(64):
            UI.chessboard.boardArray[i // 8][i % 8] = " "
        for i in range(6, len(data) - 8, 4):
            piece_color = data[i].strip()
            piece_position = data[i+1:i+3].strip()
            row =  int(piece_position[1]) - 1
            col = ord(piece_position[0]) - 97
            # Debugging statements
            print(f"Piece: {piece_color}, Position: {piece_position}, Row: {row}, Col: {col}")
            if 0 <= row < 8 and 0 <= col < 8:
                if piece_color == 'W':
                    UI.chessboard.boardArray[row][col] = "wp"
                else:
                    UI.chessboard.boardArray[row][col] = "bp"
                pawn_num += 1
            else:
                print(f"Invalid position: {piece_position}")
        UI.chessboard.round = int(time/pawn_num)
        UI.drawComponent()


    elif data == "White":
        color = "W"
        UI.playerColor = color

    elif data == "Black":
        color = "B"
        UI.playerColor = color

    elif data == "exit":
        print("Connection closed")
        break

    elif data == "Your turn":
        if game_mode == "player_vs_player":
            data, flag = UI.clientMove()  # flag = -1 lose, flag = 1 win
            if flag == -1:
                msg = "Win"
            elif flag == 1:
                msg = "Lost"
            else:
                move = ""
                move += str(chr(97 + int(data[1])))
                move += str(8 - int(data[0]))
                move += str(chr(97 + int(data[3])))
                move += str(8 - int(data[2]))
                msg = move
            msg = msg.encode()
            socketObject.send(msg)
        elif game_mode == "player_vs_agent":
            # Implement player vs agent logic
            pass
        elif game_mode == "agent_vs_agent":
            # Implement agent vs agent logic
            pass

    elif data == "Begin":
        pygame.init()  # initialize pygame
        surface = pygame.display.set_mode([600, 600], 0, 0)
        pygame.display.set_caption('Pawn Game')
        Board = ChessBoard()
        UI = UserInterface(surface, Board)
        UI.time = time
        UI.chessboard.round = int(time/14)

    elif data == "Classic":
        UI.drawComponent()

    elif data == "White's turn" or data == "Black's turn":
        pass

    elif data == "Connected to the server":
        msg = "OK"
        msg = msg.encode()
        socketObject.send(msg)


    #enemy move
    else:
        move = ""
        move += str(8 - int(data[1]))
        move += str(ord(data[0]) - 97)
        move += str(8 - int(data[3]))
        move += str(ord(data[2]) - 97)
        if int(move[1]) - int(move[3]) == 2 or int(move[1]) - int(move[3]) == -2:
            UI.chessboard.enpassant = True
            UI.chessboard.enpassantCol = int(move[0])
        UI.chessboard.changePerspective()
        UI.chessboard.computeMove(move, 0)
        UI.chessboard.changePerspective()
        UI.drawComponent()


socketObject.close()