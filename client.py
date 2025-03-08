import sys
import pygame
from board import ChessBoard
from UserInterface import UserInterface
import socket
import threading
import time as time_module



port = int(sys.argv[1]) if len(sys.argv) > 1 else 9999
game_mode = "player_vs_player"  #  mode player_vs_agent , player_vs_player, agent_vs_agent

def run_client():
    # Create a socket instance
    socketObject = socket.socket()

    # Using the socket connect to a server...in this case localhost
    socketObject.connect(("localhost", port))

    # Initialize game mode
    
    pygame.init()  # initialize pygame

    running = True  # Initialize the running flag

    try:
        while running:
            if socketObject._closed or socketObject is None:
                break
            data = socketObject.recv(1024)
            data = data.decode()

            print(data)

            if data.startswith("Time"):
                time = int(data[4:]) * 60  # Convert minutes to seconds
                print(f"Time: {time}")
            # Setup Wb4 Wa3 Wc2 Bg7 Wd4 Bg6 Be7
            elif data.startswith("Setup"):
                surface = pygame.display.set_mode([600, 600], 0, 0)
                pygame.display.set_caption('Pawn Game')
                Board = ChessBoard()
                UI = UserInterface(surface, Board)
                UI.game_mode = game_mode
                UI.socketObject = socketObject
                UI.firstgame = False
                UI.chessboard.time = time
                UI.chessboard.setup(data)
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
                UI.chessboard.changePerspective(move)
                UI.drawComponent()

            elif data == "Your turn":
                if UI.game_mode == "player_vs_player":
                    UI.drawComponent()
                    movement,flag  = UI.clientMove()
                    if flag == "W" or flag == "B":
                        msg = f"Win {flag}"
                    else:
                        msg = f"Move {movement} {UI.playerColor}"
                    msg = msg.encode()
                    socketObject.send(msg)
                elif UI.game_mode == "player_vs_agent":
                    UI.drawComponent()
                    if UI.playerColor == "W":
                        movement,flag  = UI.clientMove()
                    else:   
                        movement = UI.chessboard.ai_move(UI.playerColor)
                        print(f"AI move: {movement} color {UI.playerColor}")
                        if movement is None:
                            flag = "W"
                        else:
                            UI.chessboard.changePerspective(movement)
                            UI.drawComponent()
                            flag = UI.check_win_loss()
                    if flag == "W" or flag == "B":
                        msg = f"Win {flag}"
                    else:
                        msg = f"Move {movement} {UI.playerColor}"
                    msg = msg.encode()
                    socketObject.send(msg)
                elif UI.game_mode == "agent_vs_agent":
                    time_module.sleep(1)
                    UI.drawComponent() 
                    movement = UI.chessboard.ai_move(UI.playerColor)
                    print(f"AI move: {movement} color {UI.playerColor}")
                    if movement is None:
                        flag = "W" if UI.playerColor == "B" else "B"
                    else:
                        UI.chessboard.changePerspective(movement)
                        UI.drawComponent()
                        flag = UI.check_win_loss()
                    if flag == "W" or flag == "B":
                        msg = f"Win {flag}"
                    else:
                        msg = f"Move {movement} {UI.playerColor}"
                    msg = msg.encode()
                    socketObject.send(msg)

            elif data.startswith("Win"):
                if data[4:] == "W":
                    print("White player won")
                else:
                    print("Black player won")
                msg = str.encode("exit")
                socketObject.send(msg)
                break

            elif data == "White's turn" or data == "Black's turn":
                print("ok")

            elif data == "Connected to the server":
                print("OK")

            elif data == "exit":
                print("Connection closed")
                running = False
                break



    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        pygame.quit()
        socketObject.close()
        exit()

# Run two clients in separate threads
thread1 = threading.Thread(target=run_client)
thread2 = threading.Thread(target=run_client)

thread1.start()
thread2.start()

thread1.join()
thread2.join()