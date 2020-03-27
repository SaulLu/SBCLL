"""
This file contains the different heuristic used to evaluate boards
"""
import models.engine as engine
import models.target_engine as target_engine
from models.board import Board


def naive_heuristic(board: Board, creature='us'):
    """ A naive heuristic : calculate the difference between the number of us left and the number if them left.
    
    Arguments:
        board {Board} -- the instance of Board to evaluate
    
    Returns:
        int -- difference between the number of us left and the number of them left
    """
    number_of_us, number_of_them, _ = board.count_creatures()
    if creature == 'us':
        return number_of_us - number_of_them
    return number_of_them - number_of_us

def naive_with_humans_heuristic(board: Board, creature='us'):
    """ A naive heuristic : calculate the difference between the number of us left and the number of others left.
    
    Arguments:
        board {Board} -- the instance of Board to evaluate
    
    Returns:
        int -- difference between the number of us left and the number of others left
    """
    number_of_us, number_of_them, number_of_humans = board.count_creatures()
    if creature == 'us':
        return number_of_us - number_of_them - number_of_humans
    return number_of_them - number_of_us - number_of_humans


def distance_target_difference_heuristic(board: Board):
    return distance_target_heuristic(board, 'us') - distance_target_heuristic(board, 'them')


def distance_target_heuristic(board: Board, creature='us'):
    targets_coordinates = target_engine.get_available_targets(creature, board)
    takeover_targets = {coordinate: target_engine.get_min_takeover(board.get_cell(coordinate))
                        for coordinate in targets_coordinates}
    attackers = {coordinate: board.get_cell(coordinate).number for coordinate in board.creatures_list[creature]}
    targets_per_attackers = target_engine.get_targets_per_attackers(takeover_targets, attackers)
    return 1000 * naive_heuristic(board, creature) + __get_score_distance_target(board, targets_per_attackers)


def __get_score_distance_target(board: Board, targets_per_attackers: dict):
    score = 0
    for pos, list_targets in targets_per_attackers.items():
        for pos_target in list_targets:
            score += board.grid[pos_target].number / (engine.get_distance_between_cells(pos, pos_target) ** 2 + 1)
    return score
