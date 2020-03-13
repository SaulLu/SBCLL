"""
This file hosts the functions special to targets logic
"""
import numpy as np
import itertools
import math

from models.board import Board
from models.cell import Cell
from models.mov import Mov
import models.engine as engine

def __recursive_target_attribution(prev_attributions, remaining_creatures, available_targets):
    n_available_targets = len(available_targets)
    if remaining_creatures == 0 or n_available_targets == 0:
        return [prev_attributions + [(target, 0) for target in available_targets]]
    else:
        all_attributions = []
        target = available_targets[0]

        new_attribution = prev_attributions + [(target, 0)]
        all_attributions = all_attributions + __recursive_target_attribution(new_attribution,
                                                                             remaining_creatures,
                                                                             available_targets[1:])
        if target['min_takeover'] <= remaining_creatures:
            for i in range(target['min_takeover'], remaining_creatures + 1):
                new_attribution = prev_attributions + [(target, i)]
                all_attributions = all_attributions + __recursive_target_attribution(new_attribution,
                                                                                     remaining_creatures - i,
                                                                                     available_targets[1:])

        return all_attributions


def get_target_moves(cell: Cell, board: Board):
    min_takeover_factor = {'them': 1.5, 'humans': 1}
    creature = cell.creature
    targets = []
    for s in board.creatures_list:
        if s != creature:
            for cell_coordinates in board.creatures_list[s]:
                number = board.creatures_list[s][cell_coordinates]
                min_takeover = int(math.ceil(min_takeover_factor[s] * number))
                targets.append(
                    {'target': cell_coordinates, 'number': number, 'creature': s, 'min_takeover': min_takeover})

    global_min = min([t['min_takeover'] for t in targets])
    all_attributions = __recursive_target_attribution([], cell.number, targets)

    return all_attributions


def get_target_turns(creature, board: Board):
    targets_per_cell = []
    for x, y in board.creatures_list[creature]:
        targets_per_cell.append(get_target_moves(board.get_cell(x, y), board))
    all_attributions = []


def get_feasible_targets(board: Board, creature):
    min_takeover_factor = {engine.reverse_creature(creature): 1.5, 'humans': 1}

def get_potential_moves_from_board(board : Board, creature : string):
    targets = get_feasible_targets(board, creature) 
    return targets_to_moves(targets)