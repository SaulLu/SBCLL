import socket
import json
import pathlib
import argparse
import time



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


def receive_bye(sock):
    sock.close()


def receive_end(sock):
    # supprimertoutcequiexiste
    pass


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
        message += bytes([mov.coord_init[0]])
        message += bytes([mov.coord_init[1]])
        message += bytes([mov.number_indiv])
        message += bytes([mov.coord_arriv[0]])
        message += bytes([mov.coord_arriv[1]])
    sock.send(message)


class mov:
    def __init__(self, init, numb, arriv):
        self.coord_arriv = arriv
        self.coord_init = init
        self.number_indiv = numb



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

        dic['species'] = None  #werewolfes humans vampires
        species_alive = 0
        if n_humans:
            dic['species'] = "humans"
            species_alive += 1
        if n_vampires:
            dic['species'] = "vampires"
            species_alive += 1
        if n_werewolf:
            dic['species'] = "werewolfes"
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
    old_x = int(input("old_x?"))
    old_y = int(input("old_y?"))
    n = int(input("n?"))
    new_x = int(input("new_x?"))
    new_y = int(input("new_y?"))
    return [mov((old_x,old_y), n, (new_x, new_y))]

def run(name):
    config = load_config()
    IP, port = config["IP"], int(config["port"])

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((IP, port))
    print("Connect")
    send_nme(sock, name)

    while True:
        command = get_command(sock)
        process_command(command, sock)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('-n', '--algo_name', metavar="<algo_name>", required=True,
                        help='name of the algo', type=str)
    args = parser.parse_args()
    run(args.algo_name)
