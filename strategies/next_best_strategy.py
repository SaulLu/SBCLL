from strategies.abstract_strategy import Strategy
from models.mov import Mov
import numpy as np 
import time

class NextBestStrategy(Strategy):
    def __init__(self, max_x, max_y, heuristic):
        super().__init__(max_x, max_y, heuristic)

    def next_moves(self):
        all_possible_turns = np.array(self.engine.get_possible_turns(self.current_board, 'us'))
        all_possible_boards = [self.engine.create_possible_board_many_moves(
            self.current_board, turn, 'us') for turn in all_possible_turns]

        graded_boards = [self.heuristic(self.engine, b) for b in all_possible_boards]
        #graded_boards = list(map(lambda x: self.heuristic(self.engine, x), all_possible_boards))
        best_board_index = np.argmax(graded_boards)

        #print(all_possible_turns)
        #print(graded_boards)
        #print(all_possible_boards[-1])
        #print('\n')
        #return [Mov((5,5),5,(5,5))]
        time.sleep(0.5)
        return all_possible_turns[best_board_index]
