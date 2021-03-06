import socket
import json
import pathlib
import argparse
import time
from models.mov import Mov


def load_config():
    config_path = pathlib.Path(__file__).parent / "config.json"
    with open(config_path) as f:
        content = json.load(f)
    return content


def get_command(sock):
    command = bytes()
    while len(command) < 3:
        command += sock.recv(3 - len(command))
    return command.decode()


def get_int(sock):
    data = bytes()
    data += sock.recv(1)
    return int.from_bytes(data, byteorder='big')


def send_nme(sock, name):
    message = bytes()
    message += 'NME'.encode()
    message += bytes([len(name)])
    message += name.encode()
    sock.send(message)


def send_moves(sock, movements):
    message = bytes()
    message += 'MOV'.encode()
    message += bytes([len(movements)])
    for mov in movements:
        message += bytes([mov.initial_coordinates[0]])
        message += bytes([mov.initial_coordinates[1]])
        message += bytes([mov.n_creatures])
        message += bytes([mov.arrival_coordinates[0]])
        message += bytes([mov.arrival_coordinates[1]])
    sock.send(message)


def receive_set(sock):
    n = get_int(sock)
    m = get_int(sock)
    return n, m


def receive_hum(sock):
    n_humans = get_int(sock)
    humans_coords = [(get_int(sock), get_int(sock)) for i in range(n_humans)]
    return humans_coords


def receive_hme(sock):
    x = get_int(sock)
    y = get_int(sock)
    return x, y


def receive_upd(sock):
    n_changes = get_int(sock)
    changes_coords = []
    for i in range(n_changes):
        dic = {}
        x = get_int(sock)
        y = get_int(sock)
        n_humans = get_int(sock)
        n_vampires = get_int(sock)
        n_werewolf = get_int(sock)
        dic['coords'] = (x, y)

        dic['species'] = None  #werewolves humans vampires
        species_alive = 0
        if n_humans:
            dic['species'] = "humans"
            species_alive += 1
        if n_vampires:
            dic['species'] = "vampires"
            species_alive += 1
        if n_werewolf:
            dic['species'] = "werewolves"
            species_alive += 1

        if species_alive > 1:
            raise ValueError(f"Too many species: {n_humans} {n_vampires} {n_werewolf}")

        dic['number'] = n_humans + n_vampires + n_werewolf
        changes_coords.append(dic)
    return changes_coords


def process_command(command: str, sock):
    print(f"I recieved the command {command}")
    if command == 'SET':
        print(receive_set(sock))
    elif command == 'HUM':
        print(receive_hum(sock))
    elif command == "HME":
        print(receive_hme(sock))
    elif command == 'MAP' or command == 'UPD':
        print(receive_upd(sock))
        if command == 'UPD':
            send_moves(sock, ask_moves())


def ask_moves():
    """ask a player to play by hand"""
    moves = []
    while True:
        old_x = int(input("old_x?"))
        old_y = int(input("old_y?"))
        n = int(input("n?"))
        new_x = int(input("new_x?"))
        new_y = int(input("new_y?"))
        moves.append(Mov((old_x,old_y), n, (new_x, new_y)))
        if not "y" in input("continue (y/n) ?").lower():
            break
    return moves
