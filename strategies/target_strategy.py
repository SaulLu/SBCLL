import numpy as np
import time

from strategies.abstract_strategy import Strategy
from models.board import Board
import models.engine as engine
import models.target_engine as target_engine
from strategies.alpha_beta import AlphaBeta
from strategies.alpha_beta_breadth_first import AlphaBetaBreadthFirst


def get_random_moves_from_board(board: Board, creature: str):
    targets = []
    for _ in range(10):
        targets.append(target_engine.get_random_target_turn(board, creature))
    return target_engine.targets_to_moves(targets, board)


class TargetStrategy(Strategy):
    def __init__(self, max_x, max_y, heuristic):
        super().__init__(max_x, max_y, heuristic)

    # def get_potential_moves_from_board(self, board: Board, creature: str):
    #     targets = target_engine.get_feasible_targets(board, creature)
    #     return targets_to_moves(targets, board)

    def next_moves(self, think_time):
        alphabeta = AlphaBeta(time.time(), 4, get_random_moves_from_board, self.heuristic, 10)
        best_moves, best_score = alphabeta.alphabeta(self.current_board)        
        print(f"bestMove:{best_moves}, bestScore: {best_score}")
        return best_moves
