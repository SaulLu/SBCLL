import numpy as np
import time

from strategies.abstract_strategy import Strategy
from models.board import Board
import models.engine as engine
import models.target_engine as target_engine
from strategies.alpha_beta import AlphaBeta


def get_random_moves_from_board(board: Board, creature: str, timeout):
    targets = []
    for _ in range(10):
        targets.append(target_engine.get_random_target_turn(board, creature))
    return target_engine.targets_to_moves(targets, board)


class RandomTargetStrategy(Strategy):
    def __init__(self, max_x, max_y, heuristic):
        super().__init__(max_x, max_y, heuristic)

    def next_moves(self, think_time):
        alphabeta = AlphaBeta(time.time(), think_time, get_random_moves_from_board, self.heuristic, 5)
        best_moves, best_score = alphabeta.alphabeta(self.current_board)
        print(f"bestMove:{best_moves}, bestScore: {best_score}")
        return best_moves
