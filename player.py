import pathlib
import json

from models.board import Board
from connector.Connect import load_config as load_config_connect
from connector.Client import *

class Player():
    """Class 
    """
    def __init__(self, strategy):
        """ Constructor for player
        """
        self.our_name = None
        self.opponent_name = None
        self.first_position = None
        self.strategy = strategy
    
    def init_connection(self, ip, port):
        # call function to init the connection
        pass

    def init_board(self, max_x, max_y):
        """Function to init the board when SET is received
        Arguments:
        max_x {int} -- number of columns
        max_y {int} -- number of rows
        """
        self.strategy.current_board = Board(max_x, max_y)

    def init_humans(self, humans_coords):
        #useless apiori
        pass

    def init_home(self, x, y):
        """Function to store our info when HME is received
        
        Arguments:
            x {int} -- row
            y {[type]} -- column
        """
        self.first_position = (x,y)

    def init_game(self):
        """Initialise the game with the info received by the command 
            """
        config_connector = load_config_connect()
        config_player = self.__load_config()
        cl = Client(config_player['player_name'],config_connector['IP'],int(config_connector['port']))
        cl.start()
        #time.sleep(1)

        board_size = cl.get_board_size()
        self.init_board(board_size)
        print(f"I just got the board size: {board_size}")
    
        coords_start = cl.get_start_location()
        self.init_home(coords_start)
        print(f"I just got the starting location: {coords_start}")

        initial_setup = cl.get_board_changes(timeout = 5*60)
        for dico_cell in initial_setup:
            if dico_cell['coords'] == self.first_position:
                self.our_name = dico_cell['species']
                assert((self.our_name in ["werewolves", "vampires"]), 'Not allowed creature name')
                self.opponent_name = "werewolves" if self.our_name == "vampires" else "vampires"
        
        self.strategy.update_board(initial_setup, self.our_name)
        print(f"I just got the initial setup : {initial_setup}")

        #us vs ennemis
    
    def play(self):

        self.init_game()

        while True:
            while not(cl.is_my_turn() or cl.has_game_ended()):
                time.sleep(0.15)
            if cl.is_my_turn():
                board_changes = cl.get_board_changes()
                print(f"It's my turn, changes recieved: {board_changes}")
                self.strategy.update_board(board_changes)
                cl.put_moves_to_send(self.strategy.next_moves())
            else:
                print("game has ended")
                break

        cl.close()        
        
    def __load_config(self):
        config_path = pathlib.Path(__file__).parent.parent / "config.json"
        with open(config_path) as f:
            content = json.load(f)
        return content