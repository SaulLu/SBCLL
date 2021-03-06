import sys
import pathlib
import json
import argparse
import time

sys.path.append('.')
from models.board import Board
from connector.connect import load_config as load_config_connect
from connector.client import Client
from strategies.random_strategy import RandomStrategy
from strategies.next_best_strategy import NextBestStrategy
from strategies.random_walk_strategy import RandomWalkStrategy
from strategies.target_strategy import TargetStrategy
from strategies.target_strategy_v2 import TargetStrategy2
from strategies.random_target_strategy import RandomTargetStrategy
from strategies.heuristics import naive_heuristic 
from strategies.heuristics import distance_target_heuristic
from strategies.heuristics import distance_target_difference_heuristic


class Player:
    """Class 
    """

    def __init__(self, strategy_class, heuristic, algo_name="group_1", think_time=1.99, debug_mode=False):
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
        self.heuristic = heuristic
        self.think_time = think_time
        self.turn_num = 0
        self.debug_mode = debug_mode

    def play(self):
        """Initializes the game and loops between our turn and ennemy's turn until the end 
        """

        self.__init_game()
        try:
            while True:
                while not (self.client.is_my_turn() or self.client.has_game_ended()):
                    time.sleep(0.15)
                if self.client.is_my_turn():
                    print(f"\nIt's my turn : {self.turn_num}")
                    t0 = time.time()
                    board_changes = self.client.get_board_changes()
                    # print(f"Board changes: \n: {board_changes}")
                    self.strategy.update_board(board_changes, self.our_name)
                    next_moves = self.strategy.next_moves(self.think_time - (time.time() - t0))
                    # print(f"Next moves: \n {next_moves}")
                    self.client.put_moves_to_send(next_moves)
                    t_final = time.time() - t0
                    print(f"My turn last: {t_final}")
                    if self.debug_mode:
                        self.strategy.current_board.toxml(f'logs/map_logs/{self.turn_num}.xml')
                    self.turn_num += 2
                else:
                    print("game has ended")
                    break
        except Exception as e:
            raise e
        finally:
            self.client.close()

    def __init_game(self):
        """Initialize the game with the info received by the client 
        """
        config_connector = load_config_connect()
        config_player = self.__load_config()
        self.client = Client(self.algo_name, config_connector['IP'], int(config_connector['port']))
        self.client.start()
        time.sleep(1)  # wait a little before asking configs

        board_size = self.client.get_board_size()
        print(f"I just got the board size: {board_size}")
        self.strategy = self.strategy_class(board_size[1], board_size[0], self.heuristic)

        coords_start = self.client.get_start_location()
        self.__init_home(coords_start[0], coords_start[1])
        print("I just got the starting location")

        initial_setup = self.client.get_board_changes(timeout=5 * 60)
        for dico_cell in initial_setup:
            if dico_cell['coords'] == self.first_position:
                self.our_name = dico_cell['species']
                self.opponent_name = "werewolves" if self.our_name == "vampires" else "vampires"

        self.strategy.update_board(initial_setup, self.our_name)
        print("I just got the initial setup")
        self.turn_num = 0 if self.our_name == "vampires" else 1

    def __init_humans(self, humans_coords):
        # useless apriori
        pass

    def __init_home(self, x, y):
        """Function to store our info when HME is received
        
        Arguments:
            x {int} -- column
            y {int} -- row
        """
        self.first_position = (x, y)

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

    strategy_dic = {"default": TargetStrategy2, "random": RandomStrategy, "random_walk": RandomWalkStrategy,
                    "next_best": NextBestStrategy, "target": TargetStrategy, "target2": TargetStrategy2,
                    "random_target": RandomTargetStrategy}
    heuristics_dic = {"default": distance_target_difference_heuristic, "naive": naive_heuristic,
                      "target_diff": distance_target_difference_heuristic}

    parser = argparse.ArgumentParser()

    parser.add_argument('-n', '--algo_name', metavar="<algo_name>", required=False,
                        help='name of the algo', type=str)
    parser.add_argument('-s', '--strategy_name', metavar="<strategy_name>", required=False,
                        help=f'name of the strategy, available: {strategy_dic.keys()}', type=str)
    parser.add_argument('-he', '--heuristic', metavar="<heuristic>", required=False,
                        help=f'name of the heuristic, available: {heuristics_dic.keys()}', type=str)
    parser.add_argument("-d", "--debug", help="debug mode", action="store_true")

    args = parser.parse_args()

    if args.strategy_name:
        try:
            strategy_class = strategy_dic[args.strategy_name]
            print(f"using {args.strategy_name} strategy")
        except KeyError:
            strategy_class = strategy_dic["default"]
            print(f"using default strategy")
    else:
        strategy_class = strategy_dic["default"]
        print(f"using default strategy")

    if args.heuristic:
        try:
            heuristic = heuristics_dic[args.heuristic]
            print(f"using {args.heuristic} heuristic")
        except KeyError:
            heuristic = heuristics_dic["default"]
            print(f"using default heuristic")
    else:
        heuristic = heuristics_dic["default"]
        print(f"using default heuristic")

    if args.algo_name:
        algo_name = args.algo_name
    else:
        algo_name = "group 1"

    player = Player(strategy_class, heuristic, algo_name, think_time=1.95, debug_mode=args.debug)
    player.play()

# python player.py -s target2 -he target_diff
