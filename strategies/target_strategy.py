import numpy as np
import time

from strategies.abstract_strategy import Strategy
from models.board import Board
import models.engine as engine
import models.target_engine as target_engine
from strategies.alpha_beta import AlphaBeta
from strategies.alpha_beta_breadth_first import AlphaBetaBreadthFirst


def get_potential_moves_from_board(board: Board, creature: str, timeout):
    targets = target_engine.get_feasible_targets_turns(board, creature)
    return target_engine.targets_to_moves(targets, board)


class TargetStrategy(Strategy):
    def __init__(self, max_x, max_y, heuristic):
        super().__init__(max_x, max_y, heuristic)
        self.max_depth = 6

    def next_moves(self, think_time):
        t0 = time.time()
        alphabeta = AlphaBeta(time.time(), think_time, get_potential_moves_from_board, self.heuristic, self.max_depth)
        best_moves, best_score = alphabeta.alphabeta(self.current_board)

        print(f"best score found: {best_score}")
        if alphabeta.timed_out:
            if self.max_depth >= 4:
                self.max_depth -= 1
                print(f'max_depth changed to {self.max_depth}')
        elif (time.time() - t0 < 0.8 * think_time) and alphabeta.depth_reached >= self.max_depth:
            self.max_depth += 1
            print(f'max_depth changed to {self.max_depth}')

        return best_moves

