import math
import time
import models.target_engine as target_engine
import models.engine as engine

from strategies.alpha_beta import Node, node_pruning, AlphaBeta

class AlphaBetaBreadthFirst(AlphaBeta):
    def __init__(self, t0, timeout, get_next_moves, heuristic, max_depth):
        super().__init__(t0, timeout, get_next_moves, heuristic, max_depth)

    def alphabeta(self, root_board):
        return self.__alphabeta_gen(root_board, "us", 0, alpha=-math.inf, beta=math.inf)

    def __alphabeta_gen(self, current_board, player, current_depth, alpha, beta):
        pass

        