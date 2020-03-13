import models.engine as engine
import numpy as np
import time

from strategies.abstract_strategy import Strategy


class RandomStrategy(Strategy):
    def __init__(self, max_x, max_y, heuristic):
        super().__init__(max_x, max_y, heuristic)
        # super().__init__(new_attribute_1, new_attribute_2):

    def next_moves(self, think_time):
        all_possible_turns = engine.get_possible_turns(self.current_board, 'us')
        time.sleep(0.1)
        return all_possible_turns[np.random.randint(0, len(all_possible_turns))]
