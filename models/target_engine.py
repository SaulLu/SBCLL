"""
This file hosts the functions special to targets logic
"""
import numpy as np
import itertools
import math

from itertools import product
from typing import Type

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

def get_potential_moves_from_board(board : Board, creature : str):
    targets = get_feasible_targets(board, creature) 
    return targets_to_moves(targets)

def targets_to_moves(targets_scenarios_list: list, board:Board):
    """transforms a list of scenarios in which each cell of "us" is targeting \
        another cell into a list of move scenarios
    
    Arguments:
        targets_scenarios_list {list} -- list of scenarios in which each cell of "us" is targeting another cell
        board {Board} -- Board of the current game
    """
    calculate_moves = dict()
    mov_scenarios_list = []
    for targets_scenario in targets_scenarios_list:
        mov_scenario = []
        targets_scenario_other, targets_scenario_us = targets_scenario

        for target_dict in targets_scenario_other:
            mov_temp = target_to_move(board=board, calculate_moves=calculate_moves, \
                **target_dict)
            if mov_temp is not None:
                mov_scenario.append(mov_temp)
        
        for us_pos_dict in targets_scenario_us:
            target_cell =  __target_cell(board=board, mov_scenario=mov_scenario, \
                start=us_pos_dict['start'], target=us_pos_dict['target'])
            mov_temp = target_to_move(board=board, calculate_moves=calculate_moves, \
                start=us_pos_dict['start'], target=target_cell, \
                number=us_pos_dict['number'])
            if mov_temp is not None:
                mov_scenario.append(mov_temp)

        mov_scenarios_list.append(mov_scenario)
    return(mov_scenarios_list)

def __target_cell(board: Board, mov_scenario: list, start:(int,int), target:(int,int)):
    """Find the cell to target when the target is "us" type
    
    Arguments:
        board {Board} -- Board of the current game
        mov_scenario {list(Mov)} -- list of movements already determined for the scenario under study
        start {(int,int)} -- coordinate of us
        target {(int,int)} -- coordinate of the target
    
    Return:
        {(int,int)} -- coordinate of the cell to target
    """
    for mov in mov_scenario:
        if mov.initial_coordinates == target:
            return(mov.arrival_coordinates)
            
    poss_targets = np.array(engine.adjacent_cells(
            i_coord=start[0],
            j_coord=start[1],
            board=board
        ))

    scores = __get_scores_adjacent_cells(poss_targets, start)
    for poss_coord in scores[:,1:]:
        if not board.grid[poss_coord[0],poss_coord[1]].creature:
            target = poss_coord
            break
    return(tuple(target))

def target_to_move(board: Board, calculate_moves: dict, start:(int,int), target:(int,int), number:int):
    """[summary]
    
    Arguments:
        board {Board} -- Board of the current game
        calculate_moves {dict} -- list of movements already compute for a pair of departure and arrival coordinates
        start {(int,int)} -- coordinate of us
        target {(int,int)} -- coordinate of the target
        number {int} -- number of us from this strat coordinates targeting this target
    
    Returns:
        {Mov} -- an instance of Mov object
    """
    key = start + target

    if key in calculate_moves:
        return(calculate_moves[key])
    
    else:
        arriv = None
        target = np.array(target)

        poss_arriv = np.array(engine.adjacent_cells(
            i_coord=start[0],
            j_coord=start[1],
            board=board
        ))

        if (any((poss_arriv[:]==target).all(1))) and board.grid[target[0],target[1]].creature != 'us':
            arriv = target
            calculate_moves[key] = Mov(start, number, tuple(arriv))
            return (calculate_moves[key])

        scores = __get_scores_adjacent_cells(poss_arriv, target)
        for poss_coord in scores[:,1:]:
            if (not board.grid[poss_coord[0],poss_coord[1]].creature):
                arriv = poss_coord
                break

        if arriv.all():
            calculate_moves[key] = Mov(start, number, tuple(arriv))
        else:
            calculate_moves[key] = None
        return(calculate_moves[key])

def __get_scores_adjacent_cells(poss_arriv: np.ndarray, target:(int,int)):
    dist = get_distance_between_array_cells(poss_arriv, target)
    scores = np.column_stack((dist, poss_arriv))
    scores = scores[np.argsort(scores[:,0])]
    return(scores)

def get_distance_between_array_cells(array_pos_cell1: np.ndarray, pos_cell2):
    #asert
    return np.max(np.abs(array_pos_cell1-pos_cell2), axis=1)
