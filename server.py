import socket
import time as time_module

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
time = str.encode(time)
clients[0].send(time)
clients[1].send(time)



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

time_module.sleep(4)
# read from client connection
while (True):
    
    if player_index == 0:
        msg = str.encode("White's turn")
        clients[1].send(msg)
    else:
        msg = str.encode("Black's turn")
        clients[0].send(msg)

    msg = str.encode("Your turn")
    clients[player_index].send(msg)
    data = clients[player_index].recv(1024)
    break
    if (data != b''):

        data = data.decode()

        if data == "exit":
            msg1Bytes = str.encode("exit")
            clients[0].send(msg1Bytes)
            clients[1].send(msg1Bytes)
            print("agent wants to end the game.")
            print("Connection closed")
            break

        if data == "Win":
            if player_index:
                print("Black player won")
            else:
                print("White player won")
            msg1Bytes = str.encode("exit")
            clients[0].send(msg1Bytes)
            clients[1].send(msg1Bytes)
            break

        data = data.encode()
        msg = data
        player_index = not player_index
        clients[player_index].send(msg)
    break