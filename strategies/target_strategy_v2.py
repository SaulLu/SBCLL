
import time
import threading
import datetime

from strategies.abstract_strategy import Strategy
from models.board import Board
import models.engine as engine
import models.target_engine as target_engine
from strategies.alpha_beta import AlphaBeta
from cpp.target_module.target_module_v1 import _target_module


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


def get_potential_moves_from_board(board: Board, creature: str, timeout: float):
    player_int = 1 if creature == 'us' else 2
    units_list = construct_units_list(board)
    # log_entries(units_list, board, player_int, 'module_entries')
    targets_list = _target_module.targetsAttribution(units_list, len(units_list), player_int,
                                                     board.max_x, board.max_y, 30, 0.7 * timeout)
    targets = construct_targets(targets_list)
    # print(f"n_targets:{len(targets)}")
    # log_outputs(targets_list, targets, 'module_outputs')
    return target_engine.targets_to_moves(targets, board)


class TargetStrategy2(Strategy):
    def __init__(self, max_x, max_y, heuristic):
        super().__init__(max_x, max_y, heuristic)
        self.max_depth = 3

    def next_moves(self, think_time):
        t0 = time.time()
        alphabeta = AlphaBeta(time.time(), think_time, get_potential_moves_from_board, self.heuristic, self.max_depth)
        best_moves, best_score = alphabeta.alphabeta(self.current_board)

        if not best_moves:
            targets = [target_engine.get_random_target_turn(self.current_board, 'us')]
            best_moves = target_engine.targets_to_moves(targets, self.current_board)[0]
            print(f"random moves : {best_moves}")
        print(f"best score found: {best_score}")
        if alphabeta.timed_out:
            if self.max_depth >= 4:
                self.max_depth -= 1
                print(f'max_depth changed to {self.max_depth}')
        elif (time.time() - t0 < 0.2 * think_time) and alphabeta.depth_reached >= self.max_depth:
            self.max_depth += 2
            print(f'max_depth changed to {self.max_depth}')
        elif (time.time() - t0 < 0.8 * think_time) and alphabeta.depth_reached >= self.max_depth:
            self.max_depth += 1
            print(f'max_depth changed to {self.max_depth}')

        return best_moves
