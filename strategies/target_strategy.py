import numpy as np
import time

from strategies.abstract_strategy import Strategy
from models.board import Board
import models.engine as engine
import models.target_engine as target_engine
from strategies.alpha_beta import alphabeta

class TargetStrategy(Strategy):
    def __init__(self, max_x, max_y, heuristic):
        super().__init__(max_x, max_y, heuristic)
    
    def get_random_moves_from_board(self, board: Board, creature: str):
        targets = []
        for _ in range(10):
            targets.append(target_engine.get_random_target_turn(board, creature))
        return target_engine.targets_to_moves(targets, board)
    
    # def get_potential_moves_from_board(self, board: Board, creature: str):
    #     targets = target_engine.get_feasible_targets(board, creature)
    #     return targets_to_moves(targets, board)

    def next_moves(self, think_time):
        bestMove, bestScore = alphabeta(self.current_board, self.heuristic, self.get_random_moves_from_board, 5)