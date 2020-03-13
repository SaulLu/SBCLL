import numpy as np
import time

from strategies.abstract_strategy import Strategy
import models.engine as engine


class NextBestStrategy(Strategy):
    def __init__(self, max_x, max_y, heuristic):
        super().__init__(max_x, max_y, heuristic)

    def next_moves(self, think_time):
        all_possible_turns = np.array(engine.get_possible_turns(self.current_board, 'us'))
        all_possible_boards = [engine.create_possible_board_many_moves(
            self.current_board, turn, 'us') for turn in all_possible_turns]

        graded_boards = [self.heuristic(b) for b in all_possible_boards]
        best_board_index = np.argmax(graded_boards)
        time.sleep((think_time / 1000)/10)
        return all_possible_turns[best_board_index]
