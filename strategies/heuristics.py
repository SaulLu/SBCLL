"""
This file contains the different heuristic used to evaluate boards
"""
import models.engine as engine
import models.target_engine as target_engine
from models.board import Board


def naive_heuristic(board: Board):
    """ A naive heuristic : calculate the difference between the number of us left and the number if them left.
    
    Arguments:
        board {Board} -- the instance of Board to evaluate
    
    Returns:
        int -- difference between the number of us left and the number of them left
    """
    number_of_us, number_of_them, _ = board.count_creatures()

    return number_of_us - number_of_them


def distance_target_difference_heuristic(board: Board):
    feasible_targets_us = target_engine.get_feasible_targets(board, "us")
    feasible_targets_them = target_engine.get_feasible_targets(board, "them")

    score_us = __get_score_distance_target(board, feasible_targets_us)
    score_them = __get_score_distance_target(board, feasible_targets_them)

    return score_us - score_them


def distance_target_heuristic(board: Board):
    feasible_targets_us = target_engine.get_feasible_targets(board, "us")
    return __get_score_distance_target(board, feasible_targets_us)


def __get_score_distance_target(board: Board, dict_feasible_targets: dict):
    score = 0
    for pos, list_targets in dict_feasible_targets:
        for pos_target in list_targets:
            score += board.grid[pos_target].number / (engine.get_distance_between_cells(pos, pos_target) ** 2)
    return score
