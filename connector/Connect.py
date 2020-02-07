import socket
from time import sleep, time
from threading import Thread

IP = "127.0.0.1"
port = 5555

def getcommand(sock):
    commande = bytes()
    while len(commande)<3:
        commande += sock.recv(3-len(commande))
    return commande.decode()

def send_nme(sock, name):
    message = bytes()
    message += 'NME'.encode()
    message += bytes([len(name)])
    message += name.encode()
    sock.send(message)


def run():

    #Ajouter ici le fichier de config

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("localhost", 555))
    print("Connect")

    send_nme(sock, "test")
    print(getcommand(sock))


