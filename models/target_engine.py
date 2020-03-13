"""
This file hosts the functions special to targets logic
"""
import numpy as np
import itertools
import math

from itertools import product

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

def targets_to_moves(targets_scenarios_list, board:Board):
    mov_scenarios_list = []
    for targets_scenario in targets_scenarios_list:
        mov_scenario = []
        for target_dict in targets_scenario:
            mov_temp = target_to_move(board, **target_dict)
            if mov_temp is not None:
                mov_scenario.append(mov_temp)
        mov_scenarios_list.append(mov_scenario)
    return(mov_scenarios_list)

def target_to_move(board: Board, start, target, number:int):
    """
    
    Arguments:
        start {(int,int)} -- coordinate of us
        target {(int,int)} -- coordinate of the target
        number {int} -- number of us from this strat coordinates targeting this target
    
    Return:
        Mov -- an instance of Mov object
    """
    arriv = None
    # if target next to me

    offsets = list(product([0,1,-1],repeat = 2))
    offsets.remove((0,0))
    offsets = np.array(offsets)

    poss_arriv = start + offsets

    if target in poss_arriv and board.grid[target[0],target[1]].creature != 'us':
        arriv = target
        return (Mov(start, number, tuple(arriv)))

    dist = get_distance_between_array_cells(poss_arriv, target)
    scores = np.column_stack((dist, poss_arriv))
    scores.view('i8,i8,i8').sort(order=['f0'], axis=0)

    for poss_coord in scores[:,1:]:
        if ((poss_coord[0] >= 0) and (poss_coord[0] < board.max_x) and \
            (poss_coord[1] >= 0) and (poss_coord[1] < board.max_y) and \
            (not board.grid[poss_coord[0],poss_coord[1]].creature)):
            arriv = poss_coord
            break

    if arriv.all():
        return(Mov(start, number, tuple(arriv)))
    else:
        return(None)

def get_distance_between_array_cells(array_pos_cell1, array_pos_cell2):
        return np.max(np.abs(array_pos_cell1-array_pos_cell2), axis=1)