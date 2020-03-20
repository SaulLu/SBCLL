import numpy as np
import time

from strategies.abstract_strategy import Strategy
import models.engine as engine


class NextBestStrategy(Strategy):
    def __init__(self, max_x, max_y, heuristic):
        super().__init__(max_x, max_y, heuristic)

    def probability_score(self, probability_board):
        board, p = probability_board
        return p * self.heuristic(board)

    def next_moves(self, think_time):
        t0 = time.time()
        all_possible_turns = engine.get_possible_turns(self.current_board, 'us')
        all_possible_boards = map(lambda turn: engine.create_possible_boards_many_moves(self.current_board, turn, 'us'),
                                  all_possible_turns)
        # all_possible_boards = [engine.create_possible_boards_many_moves(
        #     self.current_board, turn, 'us') for turn in all_possible_turns]
        graded_boards = [np.sum([p*self.heuristic(board) for board,p in probability_boards]) for probability_boards
                         in all_possible_boards]
        best_board_index = np.argmax(graded_boards)
        if time.time() - t0 < think_time / 10:
            time.sleep((think_time / 1000)/10)
        return all_possible_turns[best_board_index]
