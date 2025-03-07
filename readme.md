Time 600
Setup Wb4 Wa3 Wc2 Bg7 Wd4 Bg6 Be7
Begin



# send Time x to clients
    time = input()
    time = str.encode(time)
    clients[0].send(time)
    clients[1].send(time)