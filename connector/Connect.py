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

def get_int(sock):
    data = bytes()
    data += sock.recv(1)
    return int.from_bytes(data, byteorder='big')
    
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


def recieve_set(sock):
    n = get_int(sock)
    m = get_int(sock)
    return n,m

def recieve_hum(sock):
    n_humans = get_int(sock)
    humans_coords = [(get_int(sock),get_int(sock)) for i in range(n_humans)]
    return humans_coords

def recieve_hme(sock):
    x = get_int(sock)
    y = get_int(sock)
    return x,y

def recieve_udp(sock):
    n_changes = get_int(sock)
    changes_coords = []
    for i in range(n_changes):
        dic = {}
        x = get_int(sock)
        y = get_int(sock)
        n_humans = get_int(sock)
        n_vampires = get_int(sock)
        n_werewolf = get_int(sock)
        dic['coords'] = (x,y)
        dic['spiecie'] = None # werewolfes humans vampires
        dic['number'] = n_humans + n_vampires + n_werewolf
        changes_coords.append(dic)
    return changes_coords

def process_command(command, sock):
    print(f"I recieved the command {command}")
    if command == 'SET':
        print(recieve_set(sock))
    elif command == 'HUM':
        print(recieve_hum(sock))
    elif command == "HME":
        print(recieve_hme(sock))
    elif command == 'MAP' or command == 'UDP':
        print(recieve_udp(sock))
        
def run():
    file = open("config.json", "r")
    config = json.load(file)
    IP, port = config["IP"], int(config["port"])


    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((IP, port))
    print("Connect")
    send_nme(sock, "test")
    
    while True:
        command = get_command(sock)
        process_command(command, sock)

