import socket
import threading
import queue
import copy
from connector.connect import *
import time

class ConnectProcess(threading.Thread):
    """Handle the client-serveur communication

    This class implements the class threading.Thread. It is designed to
    handle the socket communication with the serveur on a separate thread.    
    """
    
    def __init__(self, name, IP, port, sending_queue, changes_queue):
        """Constructor

        Arguments:
            name {str} -- name the algo will give to the server
            IP {str} -- IP adress of the server
            port {int} -- port of the server
            sending_queue {queue.Queue<List<move>>} -- Queue for the moves that we want to play
            changes_queue {queue.Queue<List<dict>>} -- Queue for the board changes that are send each turn
        """
        threading.Thread.__init__(self)
        self.name = name
        self.IP = IP
        self.port = port
        self.sending_queue = sending_queue
        self.changes_queue = changes_queue
        self.sock = None
        self.board_size = None
        self.human_locations = None
        self.start_location = None
        self.running = False
        self.waiting_moves = False
        self.server_closed = False
        self.game_ended = False
        
    def run(self):
        """ launch and process the communication """
        self.running = True
        self.server_closed = False
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.IP, self.port))

        send_nme(self.sock, self.name)

        while True:
            command = get_command(self.sock)
            self._process_command(command)

            if command == 'UPD':
                self.waiting_moves = True
                if not self._wait_send_moves():
                    break
            elif command == 'BYE':
                break

    def _process_command(self, command):
        """ analyse a socket command and launch the appropriate function 
            
            Arguments:
                command {str} -- 3 caracter string to designate the received command
        """
        if command == 'SET':
            self.board_size = receive_set(self.sock)
        elif command == 'HUM':
            self.human_locations = receive_hum(self.sock)
        elif command == "HME":
            self.start_location = receive_hme(self.sock)
        elif command == 'MAP' or command == 'UPD':
            new_board_changes = receive_upd(self.sock)
            self.changes_queue.put(new_board_changes)
        elif command == 'BYE':
            self.server_closed = True
            self.sending_queue.put(None)
            self.sock.close()
        elif command == 'END':
            self.game_ended = True
        else:
            raise RuntimeError(f"unknown command : {command}")

    def _wait_send_moves(self):
        """ wait for a moves and send them """
        next_moves = self.sending_queue.get()
        self.waiting_moves = False
        if next_moves is None:
            return False
        send_moves(self.sock, next_moves)
        return True

class Client:
    """Handle the communication with the server from a game logic view"""

    def __init__(self, name, IP, port):
        """Constructor

        Arguments:
            name {str} -- name the algo will give to the server
            IP {str} -- IP adress of the server
            port {int} -- port of the server
        """
        self.name = name
        self.IP = IP
        self.port = port
        self.sending_queue = queue.Queue()
        self.changes_queue = queue.Queue()
        self.connect_process = None
        self.config_wait = 0.05
        self.has_game_end = False


    def start(self):
        """ launch the ConnectProcess as a thread for communication """
        self.connect_process = ConnectProcess(self.name, self.IP, self.port, self.sending_queue, self.changes_queue)
        self.connect_process.start()

    def get_board_size(self, timeout = 5):
        """ wait for a board size to be received (with a timeout) and return it

        Arguments:
            timeout {int} -- time in seconds to wait before throwing a RuntimeError if nothin is received
        """
        if self.connect_process.running:
            t0 = time.time()
            while self.connect_process.board_size == None and time.time() - t0 < timeout:
                time.sleep(self.config_wait)
            if self.connect_process.board_size == None:
                raise RuntimeError("Could not get the board size in time")
            return self.connect_process.board_size
        else:
            raise RuntimeError("the client is not running, please call start() method first")


    def get_humans_locations(self, timeout = 5):
        """ wait for the humans locations to be received (with a timeout) and return them

        Arguments:
            timeout {int} -- time in seconds to wait before throwing a RuntimeError if nothin is received
        """
        if self.connect_process.running:
            t0 = time.time()
            while self.connect_process.human_locations == None and time.time() - t0 < timeout:
                time.sleep(self.config_wait)
            if self.connect_process.human_locations == None:
                raise RuntimeError("Could not get the humans locations in time")
            return self.connect_process.human_locations
        else:
            raise RuntimeError("the client is not running, please call start() method first")

    def get_start_location(self, timeout = 5):
        """ wait for the starting location to be received (with a timeout) and return it

        Arguments:
            timeout {int} -- time in seconds to wait before throwing a RuntimeError if nothin is received
        """
        if self.connect_process.running:
            t0 = time.time()
            while self.connect_process.start_location == None and time.time() - t0 < timeout:
                time.sleep(self.config_wait)
            if self.connect_process.start_location == None:
                raise RuntimeError("Could not get the starting location in time")
            return self.connect_process.start_location
        else:
            raise RuntimeError("the client is not running, please call start() method first")

    def get_board_changes(self, timeout = 5):
        """ wait for new board changes to be received (with a timeout) and return them

        Arguments:
            timeout {int} -- time in seconds to wait before throwing a RuntimeError if nothin is received
        """
        if self.connect_process.running:
            t0 = time.time()
            while self.changes_queue.empty() and time.time() - t0 < timeout:
                time.sleep(self.config_wait)
            if self.changes_queue.empty():
                raise RuntimeError("Could not get the board changes in time")
            return self.changes_queue.get()
        else:
            raise RuntimeError("the client is not running, please call start() method first")

    def put_moves_to_send(self, moves_to_send):
        """ add a list of moves to the sending Queue

        Arguments:
            moves_to_send {List<move>} -- moves to play that turn
        """
        if self.connect_process.running:
            self.connect_process.waiting_moves = False
            self.sending_queue.put(copy.deepcopy(moves_to_send))
        else:
            raise RuntimeError("the client is not running, please call start() method first")

    def is_my_turn(self):
        """ tell if it's the player turn """
        return self.connect_process.waiting_moves

    def has_game_ended(self):
        """ tell if the game is over """
        return self.connect_process.game_ended


    def close(self):
        """ close the communication and kill the thread """
        self.sending_queue.put(None)
    

if __name__ == '__main__':
    """play by hand

    This script uses the classes implemented above to make someone play by hand
    command: python Client.py -n <player_name>
    """
    parser = argparse.ArgumentParser()

    parser.add_argument('-n', '--algo_name', metavar="<algo_name>", required=True,
                        help='name of the algo', type=str)
    args = parser.parse_args()

    config = load_config()
    cl = Client(args.algo_name,config['IP'],int(config['port']))
    cl.start()
    time.sleep(1)
    print(f"I just got the board size: {cl.get_board_size()}")
    print(f"I just got the humans locations: {cl.get_humans_locations()}")
    print(f"I just got the starting location: {cl.get_start_location()}")

    initial_setup = cl.get_board_changes(timeout = 5*60)
    print(f"I just got the initial setup : {initial_setup}")

    while True:
        while not(cl.is_my_turn() or cl.has_game_ended()):
            time.sleep(0.15)
        if cl.is_my_turn():
            print(f"It's my turn, changes recieved: {cl.get_board_changes()}")
            cl.put_moves_to_send(ask_moves())
        else:
            print("game has ended")
            break

    cl.close()