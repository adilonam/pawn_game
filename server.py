import socket
import time as time_module
import signal
import sys
import pickle
from board import ChessBoard

clients = []
# Create a server socket

serverSocket = socket.socket()

print("Server socket created")

# Associate the server socket with the IP and Port

ip = "127.0.0.1"

# Read port from command-line arguments
port = int(sys.argv[1]) if len(sys.argv) > 1 else 9999
serverSocket.bind((ip, port))

print("Server socket bound with with ip {} port {}".format(ip, port))

# Make the server listen for incoming connections

serverSocket.listen()

# Server incoming connections "one by one"

count = 0

def signal_handler(sig, frame):
    print("Ctrl+C pressed, closing sockets...")
    for client in clients:
        client.close()
    serverSocket.close()
    print("Sockets closed")
    exit(0)

signal.signal(signal.SIGINT, signal_handler)

try:
    chessBoard = ChessBoard()
    # wait for the two agents to connect
    (clientConnection, clientAddress) = serverSocket.accept()
    count = count + 1
    clients.append(clientConnection)

    (clientConnection, clientAddress) = serverSocket.accept()
    count = count + 1
    clients.append(clientConnection)

    print("Accepted {} connections".format(count))

    msg = str.encode("Connected to the server")
    clients[0].send(msg)
    clients[1].send(msg)
    # send Time x to clients
    time = input()
    chessBoard.time = int(time[4:]) * 60
    time = str.encode(time)
    clients[0].send(time)
    clients[1].send(time)
    

    # Classic for normal board, SETUP (ends with either BLACK/WHITE) otherwise
    msg = input()
    chessBoard.setup(msg)
    msg = str.encode(msg)
    clients[0].send(msg)
    clients[1].send(msg)

    # send Begin to clients
    msg = input()
    serialized_board = pickle.dumps(chessBoard)
    clients[0].send(serialized_board)
    clients[1].send(serialized_board)
    time_module.sleep(1)

    msg = str.encode("White")
    clients[0].send(msg)
    # Serialize chessBoard and send it to clients[0]
    msg = str.encode("Black")
    clients[1].send(msg)

    player_index = 0

    
    # read from client connection
    while (True):
        time_module.sleep(1)
        if player_index == 0:
            msg = str.encode("White's turn")
            clients[1].send(msg)
        else:
            msg = str.encode("Black's turn")
            clients[0].send(msg)

        msg = str.encode("Your turn")
        clients[player_index].send(msg)
        data = clients[player_index].recv(1024)
        print(f"Data received from client: {player_index} is {data.decode()}")
        if (data != b''):
            data = data.decode()
            if data == "exit":
                msg1Bytes = str.encode("exit")
                clients[0].send(msg1Bytes)
                clients[1].send(msg1Bytes)
                print("agent wants to end the game.")
                print("Connection closed")
                break

            # elif data.startswith("Win"):
            #     print("Win received from client: ", player_index)
            #     for client in clients:
            #         client.send(str.encode(data))
            #     break
                
            elif data.startswith("Move"):
                print("Move received from client: ", player_index)
                move = data[5:]
                print(f"Move: {move}")
                player_color = "W" if player_index == 0 else "B"
                comnpute_result = chessBoard.computeMove(move, player_color)

                print(f"Compute result: {comnpute_result}")
                if comnpute_result == 0:
                    print("Invalid move")
                    clients[player_index].send(str.encode("Invalid move"))
                else:
                    if comnpute_result == 2:
                        print("En passant move")
                        chessBoard.boardArray[chessBoard.en_passant[0]][chessBoard.en_passant[1]] = " "
                        chessBoard.en_passant = None
                    chessBoard.changePerspective(move)
                    chessBoard.round += 1
                    serialized_board = pickle.dumps(chessBoard)
                    clients[0].send(serialized_board)
                    clients[1].send(serialized_board)
                    win_loss = chessBoard.check_win_loss()
                    if win_loss != "0":
                        data = f"Win {win_loss}"
                        print(f"{data}")
                        for client in clients:
                            client.send(str.encode(data))
                        break
                    player_index = 1 - player_index

except Exception as e:
    print(f"An error occurred: {e}")
finally:
    for client in clients:
        client.close()
    serverSocket.close()
    print("Sockets closed")