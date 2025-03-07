import socket
import time as time_module
import signal

clients = []
# Create a server socket

serverSocket = socket.socket()

print("Server socket created")

# Associate the server socket with the IP and Port

ip = "127.0.0.1"

port = 9991
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

    

    # Classic for normal board, SETUP (ends with either BLACK/WHITE) otherwise
    msg = input()
    msg = str.encode(msg)
    clients[0].send(msg)
    clients[1].send(msg)

    # send Begin to clients
    msg = input()
    msg = str.encode("White")
    clients[0].send(msg)
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
        print(f"Data received from client: {player_index} is {data}")
        if (data != b''):
            data = data.decode()
            if data == "exit":
                msg1Bytes = str.encode("exit")
                clients[0].send(msg1Bytes)
                clients[1].send(msg1Bytes)
                print("agent wants to end the game.")
                print("Connection closed")
                break

            elif data == "Win":
                if player_index:
                    print("Black player won")
                else:
                    print("White player won")
                msg1Bytes = str.encode("exit")
                clients[0].send(msg1Bytes)
                clients[1].send(msg1Bytes)
                break

            elif data == "Lost":
                if player_index:
                    print("White player lost")
                else:
                    print("Black player lost")
                msg1Bytes = str.encode("exit")
                clients[0].send(msg1Bytes)
                clients[1].send(msg1Bytes)
                break
            elif data.startswith("Move"):
                print("Move received from client: ", player_index)
                player_index = 1 - player_index
                clients[player_index].send(str.encode(data))
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    for client in clients:
        client.close()
    serverSocket.close()
    print("Sockets closed")