# import the socket module
import pygame
from board import ChessBoard
from UserInterface import UserInterface
import socket
import threading  # Import threading module
import time as time_module

# Create a socket instance

socketObject = socket.socket()

# Using the socket connect to a server...in this case localhost

socketObject.connect(("localhost",9991))

# Initialize game mode
game_mode = "player_vs_player"  # Default mode
pygame.init()  # initialize pygame
# Send a message to the web server to supply a page as given by Host param of GET request

running = True  # Initialize the running flag

try:
    while (running):
        if socketObject._closed or socketObject is None:
            break
        data = socketObject.recv(1024)
        data = data.decode()

        print(data)

        if data.startswith("Time"):
            time = int(data[4:]) * 60 # Convert minutes to seconds
            print(f"Time: {time}")
        # Setup Wb4 Wa3 Wc2 Bg7 Wd4 Bg6 Be7
        elif data.startswith("Setup"):
            time = 600
            surface = pygame.display.set_mode([600, 600], 0, 0)
            pygame.display.set_caption('Pawn Game')
            Board = ChessBoard()
            UI = UserInterface(surface, Board)
            UI.socketObject = socketObject
            pawn_num = 0
            UI.firstgame = False
            UI.time = time
            for i in range(64):
                UI.chessboard.boardArray[i // 8][i % 8] = " "
            for i in range(6, len(data) , 4):
                piece_color = data[i].strip()
                piece_position = data[i+1:i+3].strip()
                row = 8 - int(piece_position[1]) 
                col = ord(piece_position[0]) - 97
                # Debugging statements
                if 0 <= row < 8 and 0 <= col < 8:
                    if piece_color == 'W':
                        UI.chessboard.boardArray[row][col] = "Wp"
                    else:
                        UI.chessboard.boardArray[row][col] = "Bp"
                    pawn_num += 1
                else:
                    print(f"Invalid position: {piece_position}")
            UI.chessboard.round = int(time/pawn_num)
            UI.drawComponent()
            

        elif data == "Begin":
            print("Game started")

        elif data == "White":
            print("Player is White")
            UI.playerColor = "W"
            UI.drawComponent()

        elif data == "Black":
            print("Player is Black")
            UI.playerColor = "B"
            UI.drawComponent()

        elif data.startswith("Move"):
            move = data.split(" ")[1]
            UI.chessboard.computeMove(move, 1)
            UI.drawComponent()

        elif data == "Your turn":
            UI.drawComponent()
            if game_mode == "player_vs_player":
                is_moved , movement = UI.clientMove()
                data, flag = 100,100  # flag = -1 lose, flag = 1 win
                if flag == -1:
                    msg = "Win"
                elif flag == 1:
                    msg = "Lost"
                else:
                    msg = f"Move {movement} {UI.playerColor}"
                msg = msg.encode()
                socketObject.send(msg)
            elif game_mode == "player_vs_agent":
                # Implement player vs agent logic
                pass
            elif game_mode == "agent_vs_agent":
                # Implement agent vs agent logic
                pass

        
            

        elif data == "Classic":
            UI.drawComponent()

        elif data == "White's turn" or data == "Black's turn":
            print("ok")

        elif data == "Connected to the server":
            print("OK")


        elif data == "exit":
            print("Connection closed")
            running = False
            break

        #enemy move
        elif False:
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

except FileNotFoundError as e:
    print(f"An error occurred: {e}")
finally:
    pygame.quit()
    socketObject.close()
    exit()