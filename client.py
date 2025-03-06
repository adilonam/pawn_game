# import the socket module
import pygame
from board import ChessBoard
from UserInterface import UserInterface
import chess
import socket

global time
global color
global surface
global UI

# Create a socket instance

socketObject = socket.socket()

# Using the socket connect to a server...in this case localhost

socketObject.connect(("localhost",9999))

# Send a message to the web server to supply a page as given by Host param of GET request

while (True):

    data = socketObject.recv(1024)
    data = data.decode()

    print(data)

    if data.startswith("Time"):
        time = int(data[4:]) * 60
        msg = "OK"
        msg = msg.encode()
        socketObject.send(msg)

    elif data.startswith("Setup"):

        pawn_num = 4
        UI.firstgame = False
        for i in range(64):
            UI.chessboard.boardArray[i // 8][i % 8] = " "
        for i in range(6, len(data) - 8, 4):
            if color == 'W':
                if data[i] == color:
                    UI.chessboard.boardArray[8 - int(data[i+2])][ord(data[i + 1]) - 65] = "P"
                    pawn_num = pawn_num + 1
                else:
                    UI.chessboard.boardArray[8 - int(data[i + 2])][ord(data[i + 1]) - 65] = "p"
            else:
                if data[i] == color:
                    UI.chessboard.boardArray[int(data[i+2]) - 1][ord(data[i + 1]) - 65] = "P"
                    pawn_num = pawn_num + 1
                else:
                    UI.chessboard.boardArray[int(data[i + 2]) - 1][ord(data[i + 1]) - 65] = "p"
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
        data, flag = UI.clientMove()# flag = -1 lose, flag = 1 win
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