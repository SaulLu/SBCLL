import time
import threading
import numpy as np
import copy

from strategies.abstract_strategy import Strategy
from models.board import Board
import models.engine as engine
import models.target_engine as target_engine
from strategies.alpha_beta import AlphaBeta
from strategies.alpha_beta_breadth_first import AlphaBetaBreadthFirst
from cpp.target_module.target_module_v1 import _target_module
import datetime


def construct_units_list(board: Board):
    units_list = []
    creatures_to_int = {'humans': 0, 'us': 1, 'them': 2}
    for creature in creatures_to_int:
        for x, y in board.creatures_list[creature]:
            units_list.append([x, y, creatures_to_int[creature], board.get_cell(x=x, y=y).number])
    return units_list


def construct_targets(targets_list):
    targets = []
    for attributions_list in targets_list:
        attributions = []
        for i in range(2):
            sub_attributions = []
            for x_start, y_start, x_target, y_target, number in attributions_list[i]:
                sub_attributions.append({'start': (x_start, y_start), 'target': (x_target, y_target),
                                         'number': number})
            attributions.append(list(sub_attributions))
        targets.append(list(attributions))
    return targets


def log_entries(units_list, board: Board, player_int, filename, mode='w'):
    with open(f"logs/{filename}.csv", mode) as f:
        now = datetime.datetime.now()
        f.write(now.strftime("%Y-%m-%d %H:%M:%S:%f"))
        f.write("\ncreatures list:\n")
        f.write(str(board.creatures_list))
        f.write("\n\nunits list:\n")
        f.write(str(units_list))
        f.write("\n\nplayer int:\n")
        f.write(str(player_int))


def log_outputs(targets_list, targets, filename, mode='w'):
    with open(f"logs/{filename}.csv", mode) as f:
        now = datetime.datetime.now()
        f.write(now.strftime("%Y-%m-%d %H:%M:%S:%f"))
        f.write("\ntargets_list:\n")
        f.write(str(targets_list))
        f.write("\n\ntargets:\n")
        f.write(str(targets))


def get_potential_moves_from_board(board: Board, creature: str):
    player_int = 1 if creature == 'us' else 2
    units_list = construct_units_list(board)
    # log_entries(units_list, board, player_int, 'module_entries')
    print(f"begin c++")
    t0= time.time()
    targets_list = _target_module.targetsAttribution(units_list, len(units_list), player_int)
    print(f"end c++: {time.time()-t0}")
    targets = construct_targets(targets_list)
    # log_outputs(targets_list, targets, 'module_outputs')
    return target_engine.targets_to_moves(targets, board)


class TargetStrategy2(Strategy):
    def __init__(self, max_x, max_y, heuristic):
        super().__init__(max_x, max_y, heuristic)
        self.max_depth = 6

    def next_moves(self, think_time):
        t0 = time.time()
        best_moves, self.max_depth =  timeout(
            t0=t0,
            timeout=think_time,
            get_next_moves=get_potential_moves_from_board,
            heuristic=self.heuristic,
            max_depth=self.max_depth,
            root_board=self.current_board, 
            timeout_duration=1.99
        )

        if not best_moves:
            best_moves = [engine.get_random_turn(self.current_board, 'us')[0]]
            print(f"random moves : {best_moves}")       

        return best_moves

class AlphaBetaInterruptableThread(threading.Thread):
    def __init__(self, t0, timeout, get_next_moves, heuristic, max_depth, root_board):
        threading.Thread.__init__(self)
        self._stop_event = threading.Event()

        self.result = None
        self.alphabeta = AlphaBeta(
            t0=t0,
            timeout=timeout,
            get_next_moves=get_potential_moves_from_board,
            heuristic=heuristic,
            max_depth=max_depth
        )
        self.root_board = root_board
        self.max_depth=max_depth
        self.timeout = timeout

    def run(self):
        self.result, _ = self.alphabeta.alphabeta(self.root_board)
        if self.alphabeta.timed_out:
            if self.max_depth >= 4:
                self.max_depth -= 1
                print(f'max_depth changed to {self.max_depth}')
        elif (time.time() - self.alphabeta.t0 < 0.8 * self.timeout) and self.alphabeta.depth_reached >= self.max_depth:
            self.max_depth += 1
            print(f'max_depth changed to {self.max_depth}')
    
    def stop(self):
        self._stop_event.set()
    
    def stopped(self):
        return self._stop_event.is_set()

class RandomInterruptableThread(threading.Thread):
    def __init__(self, board):
        threading.Thread.__init__(self)
        self.result = None
        self.board = board
        self.get_random_mov = engine.get_random_mov

    def run(self):
        self.result = self.get_random_mov(self.board, "us")
    
def timeout(t0, timeout, get_next_moves, heuristic, max_depth, root_board, timeout_duration=1):
    current_board = copy.deepcopy(root_board)

    it = AlphaBetaInterruptableThread(t0, timeout, get_next_moves, heuristic, max_depth, root_board)
    rd = RandomInterruptableThread(current_board)
    it.start()
    rd.start()
    it.join(timeout_duration)
    if it.isAlive():
        print(f"kill")
        if it.max_depth > 1:
            it.max_depth -= 1
        it.stop()
        return rd.result, it.max_depth
    else:
        return it.result, it.max_depth