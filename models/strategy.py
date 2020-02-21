from abc import ABC, abstractmethod

from models.model import *
from models.engine import *


class Strategy(ABC):
    def __init__(self):
        self.engine = Engine()
        self.current_board = None
    
    @abstractmethod
    def next_moves(self):
        pass
    
    def update_board(self, list_updates, our_name):
        """Function to update the board when MAP or UPD is received
        
        Arguments:
            list_updates {list(dict)} -- list of dictionaries. Each dictionary contains information \
                in a cell that should be changed. The format used for each dictionary is \
                    {'coords': (int, int), 'species': string, 'number': int}
        """
        for update_one_cell in list_updates:
            # update_one_cell format is like {'coords': (2, 2), 'species': 'humans', 'number': 1}
            self.current_board.update_cell(update_one_cell, our_name)

class RandomStrategy(Strategy):
    def __init__(self):
        super()
        #super().__init__(new_attribute_1, new_attribute_2):

    def next_moves(self):
        #do random stuff
        pass


