import sys
sys.path.append('.')

import pathlib
import json

from models.board import Board
from connector.connect import load_config as load_config_connect
from connector.client import Client
from strategies.random_strategy import RandomStrategy
import argparse

class Player():
    """Class 
    """
    def __init__(self, strategy_class, algo_name = "group_1"):
        """ Constructor for player

        Arguments:
            strategy {Strategy} -- the instance of strategy used for this game
        """
        self.algo_name = algo_name
        self.our_name = None
        self.opponent_name = None
        self.first_position = None
        self.strategy_class = strategy_class
        self.strategy = None
        self.client = None
    
    def play(self):
        """Initializes the game and loops between our turn and ennemy's turn until the end 
        """

        try:
	        self.__init_game()

	        while True:
	            while not(self.client.is_my_turn() or self.client.has_game_ended()):
	                time.sleep(0.15)
	            if self.client.is_my_turn():
	                board_changes = self.client.get_board_changes()
	                print(f"It's my turn, changes recieved: {board_changes}")
	                self.strategy.update_board(board_changes)
	                self.client.put_moves_to_send(self.strategy.next_moves())
	            else:
	                print("game has ended")
	                break
        except Error as e:
        	print(f"got error {e}")
        	self.client.close()

        self.client.close()

    def __init_game(self):
        """Initialize the game with the info received by the client 
        """
        config_connector = load_config_connect()
        config_player = self.__load_config()
        self.client = Client(self.algo_name,config_connector['IP'],int(config_connector['port']))
        self.client.start()
        #time.sleep(1)

        board_size = self.client.get_board_size()
        print(f"I just got the board size: {board_size}")
        self.strategy = self.strategy_class(board_size[1],board_size[0])
    
        coords_start = self.client.get_start_location()
        self.__init_home(coords_start)
        print(f"I just got the starting location: {coords_start}")

        initial_setup = self.client.get_board_changes(timeout = 5*60)
        for dico_cell in initial_setup:
            if dico_cell['coords'] == self.first_position:
                self.our_name = dico_cell['species']
                assert((self.our_name in ["werewolves", "vampires"]), 'Not allowed creature name')
                self.opponent_name = "werewolves" if self.our_name == "vampires" else "vampires"
        
        self.strategy.update_board(initial_setup, self.our_name)
        print(f"I just got the initial setup : {initial_setup}")

    def __init_humans(self, humans_coords):
        #useless apriori
        pass

    def __init_home(self, x, y):
        """Function to store our info when HME is received
        
        Arguments:
            x {int} -- column
            y {int} -- row
        """
        self.first_position = (x,y)


        
    def __load_config(self):
        """Function to load the player config
        
        Returns:
            Json object -- the content of the config file
        """
        config_path = pathlib.Path(__file__).parent / "config.json"
        with open(config_path) as f:
            content = json.load(f)
        return content


if __name__ == '__main__':
    """launch a player

    This script uses the classes implemented above to make someone play by hand
    command: python Client.py -n <player_name>
    """

    strategy_dic = {"default":RandomStrategy, "random":RandomStrategy}

    parser = argparse.ArgumentParser()

    parser.add_argument('-n', '--algo_name', metavar="<algo_name>", required=True,
                        help='name of the algo', type=str)
    parser.add_argument('-s', '--strategy_name', metavar="<strategy_name>", required=True,
                        help=f'name of the strategy, avalaible: {strategy_dic.keys()}', type=str)

    args = parser.parse_args()

    try:
        strategy_class = strategy_dic[args.strategy_name]
        print(f"using {args.strategy_name} strategy")
    except KeyError:
        strategy_class = strategy_dic["default"]
        print(f"using default strategy")

    player = Player(strategy_class, args.algo_name)
    player.play()
    


    