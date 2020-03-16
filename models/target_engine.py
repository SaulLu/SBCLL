"""
This file hosts the functions special to targets logic
"""
import numpy as np
import itertools
import math
from typing import List, Set, Dict, Tuple, Optional

from itertools import product
from typing import Type

from models.board import Board
from models.cell import Cell
from models.mov import Mov
import models.engine as engine
import parameters


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


def get_available_targets(creature, board: Board):
    """
    returns the coordinates of the cells that are different from creature (humans or opponent)
    :param creature: name of the attacker
    :param board: the board to look at
    :return: List<(int,int)> list of cells' coordinates
    """
    others_creatures = itertools.chain(*[board.creatures_list[s] for s in board.creatures_list.keys() if s != creature])
    return list(others_creatures)


def get_target_turns(creature, board: Board):
    targets_per_cell = []
    for x, y in board.creatures_list[creature]:
        targets_per_cell.append(get_target_moves(board.get_cell(x=x, y=y), board))
    all_attributions = []


def get_min_takeover(cell: Cell) -> int:
    """
    compute the minimum number of creature needed to takeover a cell without a random battle
    :param cell: target cell
    :return: min_takeover
    """
    if cell.creature == 'humans':
        return math.ceil(cell.number * parameters.HUMANS_TAKEOVER_FACTOR)
    return math.ceil(cell.number * parameters.OPPONENT_TAKEOVER_FACTOR)


def assign_closest_ally(ally_coordinates: Tuple[int, int]) -> Dict:
    """
    compute for every coordinate, the closest different coordinate
    :param ally_coordinates: List of coordinate (x,y) on the Board
    :return: Dict[coordinate: Tuple[distance, closest coordinate]]
    """
    assignment = {coordinate: (np.inf, None) for coordinate in ally_coordinates}
    for i, coo1 in enumerate(ally_coordinates[:-1]):
        for coo2 in ally_coordinates[i + 1:]:
            dist = engine.travel_distance(coo1, coo2)
            if dist < assignment[coo1][0]:
                assignment[coo1] = (dist, coo2)
                assignment[coo2] = (dist, coo1)
    return assignment


def get_random_target_turn(board: Board, creature) -> Tuple[List[Dict], List[Dict]]:
    """
    return at random a target attribution for a turn
    :param board: actual board
    :param creature: attacker side
    :return: (List[Dict]],List[Dict]]) the keys of the dicts are: 'start' (coordinate of the attacker Cell),
                                    'target' (target coordinate), 'number' (number of creature to send)
                        The first List is opponent's or neutral's target, the second is friendly targets (merge intent)
    """
    targets_coordinates = get_available_targets(creature, board)
    targets = [{'coordinate': coordinate, 'min_takeover': get_min_takeover(board.get_cell(coordinate))} for coordinate
               in targets_coordinates]
    attackers = {coordinate: board.get_cell(coordinate).number for coordinate in board.creatures_list[creature]}

    attackers_possible_targets = {}
    for coordinate in attackers.keys():
        cell = board.get_cell(coordinate)
        cell_number = cell.number
        attackers_possible_targets[coordinate] = []
        for i, target in enumerate(targets):
            if cell_number >= target['min_takeover']:
                attackers_possible_targets[coordinate].append(i)

    attack_targets_attribution = []
    while len(attackers_possible_targets):

        all_attackers_coordinates = list(attackers_possible_targets.keys())
        friendly_coordinate = all_attackers_coordinates[np.random.choice(len(all_attackers_coordinates))]

        if len(attackers_possible_targets[friendly_coordinate]) == 0:  # no target for this Cell
            attackers_possible_targets.pop(friendly_coordinate)
        else:
            i_target = np.random.choice(attackers_possible_targets[friendly_coordinate])
            n_creatures = np.random.randint(targets[i_target]['min_takeover'], attackers[friendly_coordinate] + 1)

            attack_targets_attribution.append({'start': friendly_coordinate, 'target': targets[i_target]['coordinate'],
                                               'number': n_creatures})

            attackers[friendly_coordinate] -= n_creatures
            n_targets = len(attackers_possible_targets[friendly_coordinate])
            i = 0
            while i < n_targets:
                j_target = attackers_possible_targets[friendly_coordinate][i]
                if targets[j_target]['min_takeover'] > attackers[friendly_coordinate]:
                    attackers_possible_targets[friendly_coordinate].remove(j_target)
                    n_targets -= 1
                else:
                    i += 1

            for coordinate in all_attackers_coordinates:
                try:
                    attackers_possible_targets[coordinate].remove(i_target)
                except ValueError:
                    pass
                if len(attackers_possible_targets[coordinate]) == 0:
                    # if there no target anymore for the chosen cell, send every creature remaining (no left over rule)
                    if friendly_coordinate == coordinate:
                        attack_targets_attribution[-1]['number'] += attackers[friendly_coordinate]
                        attackers[friendly_coordinate] = 0
                    # remove the coordinate from possible attackers
                    attackers_possible_targets.pop(coordinate)

    merge_targets_attribution = []
    if np.sum(attackers.items()):  # if not every creature has a target:
        closest_ally = assign_closest_ally(list(attackers.keys()))
        for coordinate, n_creatures in attackers.items():
            if n_creatures and not(closest_ally[coordinate][1] is None):
                merge_targets_attribution.append({'start': coordinate, 'target': closest_ally[coordinate][1],
                                                  'number': n_creatures})

    return attack_targets_attribution, merge_targets_attribution


def __suicidal_target(targets: List[Dict], attackers: Dict) -> List[Dict]:
    friendly_coordinate = attackers.keys()[0]
    best_min_takeover = np.inf
    target_coordinate = None
    for target in targets:
        if target['min_takeover'] < best_min_takeover:
            best_min_takeover = target['min_takeover']
            target_coordinate = target['coordinate']

    return [{'start': friendly_coordinate, 'target': target_coordinate, 'number': attackers[friendly_coordinate]}]


def __recursive_attribution(targets: List[Dict], attack_targets_attribution: List[Dict], attackers: Dict,
                            attackers_possible_targets: Dict) -> List[Tuple[List[Dict], List[Dict]]]:
    if len(attackers_possible_targets) == 0:  # no more target to attack
        merge_targets_attribution = []
        if np.sum(attackers.items()):  # if not every creature has a target:
            closest_ally = assign_closest_ally(list(attackers.keys()))
            for coordinate, n_creatures in attackers.items():
                if n_creatures:
                    merge_targets_attribution.append({'start': coordinate, 'target': closest_ally[coordinate][1],
                                                      'number': n_creatures})
        if len(attackers_possible_targets) + len(merge_targets_attribution) == 0: #no target and alone
            attackers_possible_targets = __suicidal_target(targets, attackers)
        return [(attackers_possible_targets, merge_targets_attribution)]
    else:
        attribution = []


def get_feasible_targets(board: Board, creature) -> List[Tuple[List[Dict], List[Dict]]]:
    """
    return at the atrget attribution possible for a turn
    :param board: actual board
    :param creature: attacker side
    :return: [(List[Dict]],List[Dict]])] the keys of the dicts are: 'start' (coordinate of the attacker Cell),
                                    'target' (target coordinate), 'number' (number of creature to send)
                        The first List is opponent's or neutral's target, the second is friendly targets (merge intent)
    """
    targets_coordinates = get_available_targets(creature, board)
    targets = [{'coordinate': coordinate, 'min_takeover': get_min_takeover(board.get_cell(coordinate))} for coordinate
               in targets_coordinates]
    attackers = {coordinate: board.get_cell(coordinate).number for coordinate in board.creatures_list[creature]}

def targets_to_moves(targets_scenarios_list: list, board: Board):
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
            mov_temp = target_to_move(board=board, calculate_moves=calculate_moves,
                                      **target_dict)
            if mov_temp is not None:
                mov_scenario.append(mov_temp)

        for us_pos_dict in targets_scenario_us:
            if us_pos_dict['target'] is None:
                print(us_pos_dict)
            target_cell = __target_cell(board=board, mov_scenario=mov_scenario,
                                        start=us_pos_dict['start'], target=us_pos_dict['target'])
            mov_temp = target_to_move(board=board, calculate_moves=calculate_moves,
                                      start=us_pos_dict['start'], target=target_cell,
                                      number=us_pos_dict['number'])
            if mov_temp is not None:
                mov_scenario.append(mov_temp)

        mov_scenarios_list.append(mov_scenario)
    return mov_scenarios_list


def __target_cell(board: Board, mov_scenario: list, start: (int, int), target: (int, int)):
    """Find the cell to target when the target is "us" type
    
    Arguments:
        board {Board} -- Board of the current game
        mov_scenario {list(Mov)} -- list of movements already determined for the scenario under study
        start {(int,int)} -- coordinate of us
        target {(int,int)} -- coordinate of the target
    
    Return:
        {(int,int)} -- coordinate of the cell to target
    """
    target_cell = None

    for mov in mov_scenario:
        if mov.initial_coordinates == target:
            return mov.arrival_coordinates

    poss_targets = np.array(engine.adjacent_cells(
        i_coord=target[0],
        j_coord=target[1],
        board=board
    ))
    
    scores = __get_scores_adjacent_cells(poss_targets, start)
    for poss_coord in scores[:, 1:]:
        if not board.grid[poss_coord[0], poss_coord[1]].creature:
            target_cell = tuple(poss_coord)
            break
    return target_cell


def target_to_move(board: Board, calculate_moves: dict, start: (int, int), target: (int, int), number: int):
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
        return calculate_moves[key]

    else:
        arriv = None
        target = np.array(target)

        poss_arriv = np.array(engine.adjacent_cells(
            i_coord=start[0],
            j_coord=start[1],
            board=board
        ))

        if (any((poss_arriv[:] == target).all(1))) and board.grid[target[0], target[1]].creature != 'us':
            arriv = target
            calculate_moves[key] = Mov(start, number, tuple(arriv))
            return calculate_moves[key]

        scores = __get_scores_adjacent_cells(poss_arriv, target)
        for poss_coord in scores[:, 1:]:
            if not board.grid[poss_coord[0], poss_coord[1]].creature:
                arriv = poss_coord
                break

        if arriv.all():
            calculate_moves[key] = Mov(start, number, tuple(arriv))
        else:
            calculate_moves[key] = None
        return calculate_moves[key]


def __get_scores_adjacent_cells(poss_arriv: np.ndarray, target: (int, int)):
    dist = get_distance_between_array_cells(poss_arriv, target)
    scores = np.column_stack((dist, poss_arriv))
    scores = scores[np.argsort(scores[:,0])]
    return(scores)
    

def get_distance_between_array_cells(array_pos_cell1: np.ndarray, pos_cell2):
    # asert
    return np.max(np.abs(array_pos_cell1 - pos_cell2), axis=1)
