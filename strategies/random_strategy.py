
from strategies.abstract_strategy import Strategy
import numpy as np 

class RandomStrategy(Strategy):
    def __init__(self,max_x, max_y):
        super(max_x, max_y)
        #super().__init__(new_attribute_1, new_attribute_2):

    def next_moves(self):
        all_possibles_moves = self.engine.get_all_possible_moves(self.board)

        return all_possibles_moves[np.random.randint(len(all_possibles_moves))]