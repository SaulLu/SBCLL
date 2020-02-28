from strategies.abstract_strategy import Strategy
import numpy as np 

class NextBestStrategy(Strategy):
    def __init__(self, max_x, max_y, heuristic):
        super().__init__(max_x, max_y, heuristic)

    def next_moves(self):
        all_possible_turns = np.array(self.engine.get_possible_turns(self.current_board, 'us'))
        all_possible_boards = [self.engine.create_possible_board_many_moves(
            self.current_board, turn, 'us') for turn in all_possible_turns]

        graded_boards = np.array(map(lambda x: self.heuristic(self.engine, x), all_possible_boards))
        best_board_index = np.argmax(graded_boards)
        return all_possible_turns[best_board_index]
