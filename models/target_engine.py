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


def get_available_targets(creature, board: Board):
    """
    returns the coordinates of the cells that are different from creature (humans or opponent)
    :param creature: name of the attacker
    :param board: the board to look at
    :return: List<(int,int)> list of cells' coordinates
    """
    others_creatures = itertools.chain(*[board.creatures_list[s] for s in board.creatures_list.keys() if s != creature])
    return list(others_creatures)


def get_min_takeover(cell: Cell) -> int:
    """
    compute the minimum number of creature needed to takeover a cell without a random battle
    :param cell: target cell
    :return: min_takeover
    """
    if cell.creature == 'humans':
        return math.ceil(cell.number * parameters.HUMANS_TAKEOVER_FACTOR)
    return math.ceil(cell.number * parameters.OPPONENT_TAKEOVER_FACTOR)


def assign_closest_ally(ally_coordinates: List[Tuple[int, int]]) -> Dict:
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


def __suicidal_target(takeover_targets: Dict, attackers: Dict) -> List[Dict]:
    """
    Find the opponent target with the lowest number of creature
    :param takeover_targets:
    :param attackers:
    :return:
    """
    friendly_coordinate = list(attackers.keys())[0]
    best_min_takeover = np.inf
    target_coordinate = None
    for target, min_takeover in takeover_targets.items():
        if min_takeover < best_min_takeover:
            best_min_takeover = min_takeover
            target_coordinate = target

    return [{'start': friendly_coordinate, 'target': target_coordinate, 'number': attackers[friendly_coordinate]}]


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
            if n_creatures and not (closest_ally[coordinate][1] is None):
                merge_targets_attribution.append({'start': coordinate, 'target': closest_ally[coordinate][1],
                                                  'number': n_creatures})

    if len(attack_targets_attribution) + len(merge_targets_attribution) == 0:  # no target and alone
        takeover_targets = {coordinate: get_min_takeover(board.get_cell(coordinate)) for coordinate in
                            targets_coordinates}
        attack_targets_attribution = __suicidal_target(takeover_targets, attackers)
    return attack_targets_attribution, merge_targets_attribution


def get_targets_per_attackers(takeover_targets: Dict, attackers: Dict) -> Dict:
    """
    Look which targets can be aimed at by the attackers
    :param takeover_targets: dict with target coordinate as key and min_takeover as value
    :param attackers: dict with attacker coordinate  as key and attacker number as value
    :return: Dict with attacker coordinate as key and a List of targets coordinates as value
    """
    targets_per_attackers = {}
    for attacker_coo, n_creature in attackers.items():
        targets_per_attackers[attacker_coo] = [target_coo for target_coo, min_takeover in takeover_targets.items()
                                               if n_creature >= min_takeover]
    return targets_per_attackers


def get_attackers_per_targets(takeover_targets: Dict, attackers: Dict) -> Dict:
    """
    Look which attackers can aim at which target
    :param takeover_targets: dict with target coordinate as key and min_takeover as value
    :param attackers: dict with attacker coordinate  as key and attacker number as value
    :return: Dict with target coordinate as key and a List of attackers coordinates as value
    """
    attackers_per_targets = {}
    for target_coo, min_takeover in takeover_targets.items():
        attackers_per_targets[target_coo] = [att_coo for att_coo, att_number in attackers.items()
                                             if att_number >= min_takeover]
    return attackers_per_targets


def _get_next_target(attackers_per_targets: Dict) -> Optional[Tuple[int, int]]:
    """
    return the next target with possible attackers
    :param attackers_per_targets: Dict with target coordinate as key and a List of attackers coordinates as value
    :return: None or the next target
    """
    for target_coo in attackers_per_targets.keys():
        if len(attackers_per_targets[target_coo]):
            return target_coo
    return None


def _update_recursive_attributes(takeover_targets: Dict, temp_attribution: List[Dict], attackers: Dict,
                                 attackers_per_target: Dict, targets_per_attacker: Dict, target: Tuple,
                                 attacker: Tuple, n_creature: int) -> Tuple:
    # deepcopy
    updated_attribution = [dict(d) for d in temp_attribution]
    updated_attackers = dict(attackers)
    updated_attackers_per_target = {k: list(L) for k, L in attackers_per_target.items()}
    updated_targets_per_attacker = {k: list(L) for k, L in targets_per_attacker.items()}

    updated_attackers_per_target[target] = []
    infer = False
    if n_creature:
        # update the per target
        updated_attackers[attacker] -= n_creature
        for t, min_takeover in takeover_targets.items():
            if min_takeover > updated_attackers[attacker]:
                try:
                    updated_attackers_per_target[t].remove(attacker)  # attacker has no more the number to attack this t
                    updated_targets_per_attacker[attacker].remove(t)
                    infer = len(updated_attackers_per_target[t]) == 0
                except ValueError:
                    pass

        # update per attacker
        for a in targets_per_attacker.keys():
            try:
                updated_targets_per_attacker[a].remove(target)  # only one attacker per target
            except ValueError:
                pass

        # update attribution
        updated_attribution.append({'start': attacker, 'target': target, 'number': n_creature})

    return infer, (updated_attribution, updated_attackers, updated_attackers_per_target, updated_targets_per_attacker)


def _recursive_target_attribution(takeover_targets: Dict, temp_attribution: List[Dict], attackers: Dict,
                                  attackers_per_target: Dict, targets_per_attacker: Dict) -> List:
    """
    recursivly attribute targets to cells
    :param takeover_targets:
    :param temp_attribution:
    :param attackers:
    :param attackers_per_target:
    :param targets_per_attacker:
    :return:
    """
    next_target = _get_next_target(attackers_per_target)
    if next_target is not None:
        attributions = []
        min_takeover = takeover_targets[next_target]
        infer = False
        for attacker_coo in attackers_per_target[next_target]:
            # print(f"next_target:{next_target}, att {attacker_coo}, call: {n_call}")
            try:
                min_other_takeover = np.min([takeover_targets[t] for t in
                                             targets_per_attacker[attacker_coo] if t != next_target])
            except ValueError:
                min_other_takeover = 0
            max_partial_attribution = attackers[attacker_coo] - min_other_takeover  # no left over

            creature_values = [attackers[attacker_coo]]
            if min_other_takeover:
                creature_values = list(range(min_takeover, max_partial_attribution + 1)) + creature_values

            for n_creature in creature_values:
                updated_infer, updated_attributes = _update_recursive_attributes(takeover_targets, temp_attribution,
                                                                                 attackers, attackers_per_target,
                                                                                 targets_per_attacker, next_target,
                                                                                 attacker_coo, n_creature)
                infer = infer or updated_infer
                new_attributions = _recursive_target_attribution(takeover_targets, *updated_attributes)
                attributions = attributions + new_attributions

        if infer:
            _, updated_attributes = _update_recursive_attributes(takeover_targets, temp_attribution, attackers,
                                                                 attackers_per_target, targets_per_attacker,
                                                                 next_target, (None, None), 0)
            new_attributions = _recursive_target_attribution(takeover_targets, *updated_attributes)
            attributions = attributions + new_attributions

        return attributions
    else:  # No more target to be aimed at
        effective_attackers = {target['start'] for target in temp_attribution}
        merge_targets_attribution = []
        updated_attribution = [dict(d) for d in temp_attribution]
        if np.sum(attackers.items()):  # if not every creature has a target:
            closest_ally = assign_closest_ally(list(attackers.keys()))
            for coordinate, n_creatures in attackers.items():
                if n_creatures and not (closest_ally[coordinate][1] is None):
                    if coordinate in effective_attackers:
                        return []
                    merge_targets_attribution.append({'start': coordinate, 'target': closest_ally[coordinate][1],
                                                      'number': n_creatures})

        if len(temp_attribution) + len(merge_targets_attribution) == 0:  # no target and alone
            updated_attribution = __suicidal_target(takeover_targets, attackers)
        return [[updated_attribution, merge_targets_attribution]]


def get_feasible_targets_turns(board: Board, creature) -> List[Tuple[List[Dict], List[Dict]]]:
    """
    return all the feasible target attribution possible for a turn
    :param board: actual board
    :param creature: attacker side
    :return: [(List[Dict]],List[Dict]])] the keys of the dicts are: 'start' (coordinate of the attacker Cell),
                                    'target' (target coordinate), 'number' (number of creature to send)
                        The first List is opponent's or neutral's target, the second is friendly targets (merge intent)
    """
    targets_coordinates = get_available_targets(creature, board)
    takeover_targets = {coordinate: get_min_takeover(board.get_cell(coordinate)) for coordinate in targets_coordinates}
    attackers = {coordinate: board.get_cell(coordinate).number for coordinate in board.creatures_list[creature]}
    attackers_per_target = get_attackers_per_targets(takeover_targets, attackers)
    targets_per_attackers = get_targets_per_attackers(takeover_targets, attackers)

    return _recursive_target_attribution(takeover_targets, [], attackers, attackers_per_target, targets_per_attackers)


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
    try:
        key = start + target
    except Exception as e:
        print("start", start)
        print("target", target)
        raise e

    if key in calculate_moves:
        if calculate_moves:
            return Mov(start, number, calculate_moves[key])
        return None
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
            calculate_moves[key] = tuple(arriv)
            return Mov(start, number, calculate_moves[key])

        scores = __get_scores_adjacent_cells(poss_arriv, target)
        for poss_coord in scores[:, 1:]:
            if not board.grid[poss_coord[0], poss_coord[1]].creature:
                arriv = poss_coord
                break
        try:
            if not isinstance(arriv, type(None)):
                calculate_moves[key] = tuple(arriv)
            else:
                calculate_moves[key] = None
        except Exception as e:
            print(start, target, number)
            raise e
        return Mov(start, number, calculate_moves[key])


def __get_scores_adjacent_cells(poss_arriv: np.ndarray, target: (int, int)):
    dist = get_distance_between_array_cells(poss_arriv, target)
    scores = np.column_stack((dist, poss_arriv))
    scores = scores[np.argsort(scores[:, 0])]
    return (scores)


def get_distance_between_array_cells(array_pos_cell1: np.ndarray, pos_cell2):
    # asert
    return np.max(np.abs(array_pos_cell1 - pos_cell2), axis=1)
