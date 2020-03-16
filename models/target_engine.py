"""
This file hosts the functions special to targets logic
"""
import numpy as np
import itertools
import math
from typing import List, Set, Dict, Tuple, Optional

from models.board import Board
from models.cell import Cell
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


def assign_closest_ally(ally_coordinates: Tuple[int,int]) -> Dict:
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
            if n_creatures:
                merge_targets_attribution.append({'start': coordinate, 'target': closest_ally[coordinate][1],
                                                  'number': n_creatures})

    return attack_targets_attribution, merge_targets_attribution


def get_feasible_targets(board: Board, creature) -> List[Tuple[List[Dict], List[Dict]]]:
    """
    compute
    :param board: actual board
    :param creature: attacker side
    :return:
    """
    targets_coordinates = get_available_targets(creature, board)
    targets = [{'coordinates': coordinate, 'min_takeover': get_min_takeover(board.get_cell(coordinate))} for coordinate
               in targets_coordinates]
