import time
import queue

from cpp.target_module.target_module_v1 import _target_module
from speed_test import loadMap
from strategies.target_strategy_v2 import construct_units_list, construct_targets, get_potential_moves_from_board
from models import target_engine
from models.board import Board
from strategies.caller import GetNextMoveCaller


def print_targets(targets_list):
    for attack, merge in targets_list:
        print('\nattacks:')
        for d in attack:
            print(d)
        print('merge:')
        for d in merge:
            print(d)


def test_duplicates_from_board(board, creature):
    print(board)
    t0 = time.time()
    player_int = 1 if creature == 'us' else 2
    units_list = construct_units_list(board)
    targets_list = _target_module.targetsAttribution(units_list, len(units_list), player_int)
    targets = construct_targets(targets_list)
    print(f"C++: I have found {len(targets_list)} targets scenarios in {time.time() - t0} seconds")
    ids = set()
    for targets_turn in targets:
        id_turn = turn_to_id(targets_turn)
        if id_turn in ids:
            print(targets_turn)
        else:
            ids.add(id_turn)
        ids.add(id_turn)
    print(f"duplicates: {len(targets) - len(ids)}")

    t0 = time.time()
    targets = target_engine.get_feasible_targets_turns(board, creature)
    print(f"Python: I have found {len(targets)} targets scenarios in {time.time() - t0} seconds")

def module_test():
    units_list = [[5, 1, 1, 11], [1, 7, 2, 19], [6, 2, 2, 6]]
    player_int = 2
    all_attributions = _target_module.targetsAttribution(units_list, len(units_list), player_int, 22.5, 2)
    for attacks, merges in all_attributions:
        print('\nattacks:')
        for x_start, y_start, x_target, y_target, number in attacks:
            print(f"\tstart:({x_start}, {y_start}), target:({x_target}, {y_target}), number: {number}")
        print('merges:')
        for x_start, y_start, x_target, y_target, number in merges:
            print(f"\tstart:({x_start}, {y_start}), target:({x_target}, {y_target}), number: {number}")
    print('end')


def test1():
    creature = 'us'
    max_x, max_y, board = loadMap('test_maps/map_10_10_8.xml')

    t0 = time.time()
    player_int = 1 if creature == 'us' else 2
    units_list = construct_units_list(board)
    targets_list = _target_module.targetsAttribution(units_list, len(units_list), player_int)
    targets = construct_targets(targets_list)
    print(f"C++: I have found {len(targets_list)} targets scenarios in {time.time() - t0} seconds")

    t0 = time.time()
    targets = target_engine.get_feasible_targets_turns(board, creature)
    print(f"Python: I have found {len(targets)} targets scenarios in {time.time() - t0} seconds")


def test2():
    creature = 'us'
    max_x, max_y, = 10, 10
    units_list = [[0, 5, 0, 17], [1, 0, 0, 2], [1, 7, 0, 3], [2, 1, 0, 4], [2, 8, 0, 4], [3, 8, 0, 3], [4, 3, 0, 17],
                  [5, 6, 0, 17], [6, 1, 0, 3], [7, 1, 0, 4], [7, 8, 0, 4], [8, 2, 0, 3], [8, 9, 0, 2], [9, 4, 0, 17],
                  [1, 4, 1, 10], [1, 6, 1, 5], [7, 3, 2, 4], [8, 5, 2, 11]]
    board = Board.from_units_list(units_list, max_x, max_y)
    print(board)

    t0 = time.time()
    player_int = 1 if creature == 'us' else 2
    units_list = construct_units_list(board)
    targets_list = _target_module.targetsAttribution(units_list, len(units_list), player_int)
    targets = construct_targets(targets_list)
    print(f"C++: I have found {len(targets_list)} targets scenarios in {time.time() - t0} seconds")

    ids = set()
    for targets_turn in targets:
        id_turn = turn_to_id(targets_turn)
        ids.add(id_turn)
    print(f"duplicates: { len(targets) - len(ids)}, uniques: {len(ids)}")

    t0 = time.time()
    targets = target_engine.get_feasible_targets_turns(board, creature)
    print(f"Python: I have found {len(targets)} targets scenarios in {time.time() - t0} seconds")


def test3():
    creature = 'us'
    max_x, max_y, = 10, 10
    units_list = [[1, 0, 0, 2], [1, 7, 0, 3], [8, 2, 0, 3], [1, 4, 1, 6], [1, 6, 1, 5], [7, 3, 2, 4]]
    board = Board.from_units_list(units_list, max_x, max_y)
    test_duplicates_from_board(board, creature)


def test4():
    creature = 'us'
    max_x, max_y, board = loadMap('test_maps/map_10_10_8.xml')
    test_duplicates_from_board(board, creature)


def turn_to_id(turn):
    attacks, merges = turn
    all_tuple = [d['start'] + d['target'] + tuple([d['number']]) for L in turn for d in L]
    all_tuple.sort()
    return tuple(all_tuple)


def trad():
    units_list = [[5, 1, 1, 11], [1, 7, 2, 19], [6, 2, 2, 6]]
    s = str(units_list)
    s = s.replace('[', '{')
    s = s.replace(']', '}')
    print("{", s, "};")

def interrupt():
    player = 'us'
    max_x, max_y, board = loadMap('test_maps/testmap2.xml', "Vampires")
    allowed_time = 2
    t0 = time.time()
    caller = GetNextMoveCaller(get_potential_moves_from_board, board, player, allowed_time)
    caller.start()
    list_moves = []
    while time.time() - t0 < allowed_time and len(list_moves) == 0:
        try:
            list_moves = caller.next_moves.get(timeout=0.001)
        except queue.Empty:
            pass
    print(f"time: {time.time() - t0}")
    print(f"size_list_moves: {len(list_moves)}")
    caller.kill()
    print(f"time: {time.time() - t0}")
    caller.join()
    print(f"time: {time.time() - t0}")


if __name__ == "__main__":
    interrupt()
