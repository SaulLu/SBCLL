from abc import ABC, abstractmethod

from models.board import Board
from models.engine import Engine


class Strategy(ABC):
    """Abstract class to implement player strategy
    """
    def __init__(self):
        """Strategy class constructor
        """
        self.engine = Engine()
        self.current_board = None
    
    @abstractmethod
    def next_moves(self):
        """Function to overide. Should return dictionnary of moves to play
        """
        pass
    
    def update_board(self, list_updates, our_name):
        """Function to update the board when MAP or UPD is received
        
        Arguments:
            list_updates {list(dict)} -- list of dictionaries. Each dictionary contains information \
                in a cell that should be changed. The format used for each dictionary is \
                    {'coords': (int, int), 'species': string, 'number': int}
            our_name {string} -- our species name to anonymize
        """
        for update_one_cell in list_updates:
            # update_one_cell format is like {'coords': (2, 2), 'species': 'humans', 'number': 1}
            self.current_board.update_cell(update_one_cell, our_name)




