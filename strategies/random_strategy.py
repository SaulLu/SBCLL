
from strategies.abstract_strategy import Strategy
import numpy as np 

class RandomStrategy(Strategy):
    def __init__(self, max_x, max_y):
        super(max_x, max_y)
        #super().__init__(new_attribute_1, new_attribute_2):

    def next_moves(self):
        all_possible_turns = self.engine.get_possible_turns(self.board)
        return all_possible_turns[np.random.randint(len(all_possible_turns))]