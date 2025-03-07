Time 600
Setup Wd4 Be7
Begin



# send Time x to clients
    time = input()
    time = str.encode(time)
    clients[0].send(time)
    clients[1].send(time)