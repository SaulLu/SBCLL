import socket
import sys
import json
from time import sleep, time
from threading import Thread

def get_command(sock):
    command = bytes()
    while len(command)<3:
        command += sock.recv(3-len(command))
    return command.decode()

def receive_bye(sock):
    sock.close()

def receive_end(sock):
    #supprimertoutcequiexiste
    pass

def send_nme(sock, name):
    message = bytes()
    message += 'NME'.encode()
    message += bytes([len(name)])
    message += name.encode()
    sock.send(message)

def send_mov(sock, movements):
    message = bytes()
    message += 'MOV'.encode()
    message += bytes([len(movements)])
    for mov in movements:
        message += mov.coord_init.encode()
        message += mov.number_indiv.encode()
        message += mov.coord_arriv.encode()
    sock.send(message)


def run():
    file = open("config.json", "r")
    config = json.load(file)
    IP, port = config["IP"], int(config["port"])


    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((IP, port))
    print("Connect")
    send_nme(sock, "test")
    print(get_command(sock))


