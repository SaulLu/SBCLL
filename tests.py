import numpy as np

from models.cell import Cell
from models.board import Board
import models.engine as engine
import models.target_engine as target_engine
from strategies.heuristics import naive_heuristic
from strategies.heuristics import distance_target_heuristic
from strategies.random_target_strategy import get_random_moves_from_board
from models.mov import Mov


def __create_random_board(max_x, max_y):
    board = Board(max_x, max_y)
    for _ in range(20):
        species = [None, 'us', 'them', 'humans']
        s = species[np.random.randint(len(species))]
        if s is None:
            number = 0
        else:
            number = np.random.randint(10)
        board.update_cell2(Cell(np.random.randint(max_x), np.random.randint(max_y), s, number))
    n_us, n_them, n_h = board.count_creatures()
    if n_us * n_them == 0:
        board = __create_random_board(max_x, max_y)
    return board


def board_test_1():
    max_x = 5
    max_y = 5
    board = Board(max_x, max_y)
    our_name = 'vampires'
    for i in range(5000):
        if np.random.rand() > 0.5:
            species = [None, 'us', 'them', 'humans']
            s = species[np.random.randint(len(species))]
            if s is None:
                number = 0
            else:
                number = np.random.randint(10)
            board.update_cell2(Cell(np.random.randint(max_x), np.random.randint(max_y), s, number))
        else:
            species = [None, 'vampires', 'werewolves', 'humans']
            s = species[np.random.randint(len(species))]
            if s is None:
                number = 0
            else:
                number = np.random.randint(10)
            board.update_cell((np.random.randint(max_x), np.random.randint(max_y)), s, number, our_name)

        if engine.count_creatures(board) != board.count_creatures():
            print(board)
            print(engine.count_creatures(board))
            print(board.count_creatures())
            print(board.creatures_list)
            raise RuntimeError("creature count error")


def random_target_test_2():
    max_x = 6
    max_y = 5
    board = Board(max_x, max_y)
    our_name = 'vampires'

    board.update_cell((2, 2), 'humans', 1, our_name)
    board.update_cell((3, 3), 'humans', 1, our_name)
    board.update_cell((4, 4), 'humans', 1, our_name)
    board.update_cell((5, 3), 'humans', 1, our_name)

    board.update_cell((5, 4), 'vampires', 2, our_name)
    board.update_cell((2, 3), 'werewolves', 2, our_name)
    print(board)
    for i in range(5000):
        moves = get_random_moves_from_board(board, 'us')[0]
        board = engine.create_possible_boards_many_moves(board, moves, 'us')

        for x in range(max_x):
            for y in range(max_y):
                if board.grid[x][y].number < 0:
                    print(board)
                    print(moves)
                    raise RuntimeError


def distance_target_heuristic_test_1():
    board = __create_random_board(6, 9)
    print(distance_target_heuristic(board))


def check_targets(board, targets):
    attack_targets, merge_targets = targets
    sending_per_start = {}
    for target in attack_targets:
        try:
            sending_per_start[target['start']] += target['number']
        except KeyError:
            sending_per_start[target['start']] = target['number']
        if target['number'] < target_engine.get_min_takeover(board.get_cell(target['target'])):
            raise RuntimeError(f"unfeasible target: {target} \n {board}")

    for target in merge_targets:
        try:
            sending_per_start[target['start']] += target['number']
        except KeyError:
            sending_per_start[target['start']] = target['number']

    for start, number_sent in sending_per_start.items():
        if number_sent > board.get_cell(start).number:
            raise RuntimeError("sending too many creatures: start: {start}, number: {number} \n {board}")


def random_targets_test():
    for k in range(50):
        board = Board(10, 3)
        n_humans = np.random.randint(5, 10)
        n_werewolves = np.random.randint(5, 10)
        vampires = np.random.randint(5, 10)

        for i in range(n_humans):
            board.update_cell((i, 0), "humans", np.random.randint(1, 5), "vampires")
        for i in range(n_werewolves):
            board.update_cell((i, 1), "werewolves", np.random.randint(1, 10), "vampires")
        for i in range(vampires):
            board.update_cell((i, 2), "vampires", np.random.randint(1, 10), "vampires")

        for i in range(100):
            check_targets(board, target_engine.get_random_target_turn(board, 'us'))


def esperance_tests():
    board = Board(5, 5)

    board.update_cell((1, 4), "humans", 2, "vampires")
    board.update_cell((4, 4), "humans", 2, "vampires")
    board.update_cell((1, 3), "werewolves", 10, "vampires")
    board.update_cell((3, 3), "werewolves", 4, "vampires")
    board.update_cell((2, 3), "humans", 4, "vampires")
    board.update_cell((1, 1), "werewolves", 4, "vampires")
    board.update_cell((1, 2), "humans", 5, "vampires")

    init_cell = (1, 3)
    target_cell = (2, 3)

    # print("--before move--")
    # print("init", board.get_cell(coordinate=init_cell))
    # print("target", board.get_cell(coordinate=target_cell))

    move = Mov(init_cell, 3, target_cell)
    # engine.apply_possible_board_one_move(board, move, "them", output_species="us", output_qty=2)
    # engine.apply_possible_board_one_move(board, move, "them")

    # print("--after move--")
    # print("init", board.get_cell(coordinate=init_cell))
    # print("target", board.get_cell(coordinate=target_cell))

    # print(engine.create_possible_boards_one_move(board, move, "them", method="esperance"))

    other_move = Mov((1, 1), 3, (1, 2))
    moves_list = [move, other_move]

    # print(engine.create_possible_boards_many_moves(board, moves_list, "them"))
    # print(engine.create_possible_boards_many_moves(board, moves_list, "them", method="esperance"))


def test_negatif():
    board = Board(5, 5)
    our_name = 'vampires'
    board.update_cell((1, 4), "humans", 2, "vampires")
    board.update_cell((4, 4), "humans", 2, "vampires")
    board.update_cell((1, 3), "werewolves", 10, "vampires")
    board.update_cell((3, 3), "werewolves", 4, "vampires")
    board.update_cell((2, 3), "humans", 4, "vampires")
    board.update_cell((1, 1), "werewolves", 4, "vampires")
    board.update_cell((1, 2), "humans", 5, "vampires")

    for i in range(1000):
        moves = get_random_moves_from_board(board, "them")

        count = 0
        for move in moves[0]:
            engine.apply_possible_board_one_move(board, move, "them")
            for x in range(board.max_x):
                for y in range(board.max_y):
                    cell = board.get_cell((x, y))
                    if cell.number < 0:
                        print("negative people")
                        print(move)
                        print(board)
                        count += 1
    print("count", count)


def ramdom_moves_test():
    board = Board(5, 5)
    creature = 'them'
    board.update_cell((1, 4), "humans", 2, "vampires")
    board.update_cell((4, 4), "humans", 2, "vampires")
    board.update_cell((1, 3), "werewolves", 10, "vampires")
    board.update_cell((3, 3), "werewolves", 4, "vampires")
    board.update_cell((2, 3), "humans", 4, "vampires")
    board.update_cell((1, 1), "werewolves", 4, "vampires")
    board.update_cell((1, 2), "vampires", 5, "vampires")
    print(get_random_moves_from_board(board, creature))


def target_to_move_test():
    board = Board(5, 5)

    board.update_cell((1, 4), "humans", 2, "vampires")
    board.update_cell((4, 4), "humans", 2, "vampires")
    board.update_cell((1, 3), "werewolves", 1, "vampires")
    board.update_cell((3, 3), "werewolves", 4, "vampires")
    board.update_cell((2, 2), "vampires", 4, "vampires")

    print(board)
    calculate_moves = dict()
    config = {
        'calculate_moves': calculate_moves,
        'start': (1, 3),
        'target': (2, 2),
        'number': 2
    }
    # print("Moves for the scenario")
    # print(target_engine.target_to_move(board, **config))


def targets_to_move_test():
    board = Board(5, 5)

    board.update_cell((1, 4), "humans", 2, "vampires")
    board.update_cell((4, 4), "humans", 2, "vampires")
    board.update_cell((1, 3), "werewolves", 1, "vampires")
    board.update_cell((3, 3), "werewolves", 4, "vampires")
    board.update_cell((2, 2), "vampires", 4, "vampires")

    print(board)

    targets_scenarios_list = [
        [
            [{
                'start': (1, 3),
                'target': (2, 2),
                'number': 1
            },
                {
                    'start': (3, 3),
                    'target': (1, 4),
                    'number': 3
                }],
            []
        ],
        [
            [{
                'start': (1, 3),
                'target': (1, 4),
                'number': 1
            },
                {
                    'start': (3, 3),
                    'target': (1, 4),
                    'number': 3
                }],
            [
                {
                    'start': (1, 3),
                    'target': (3, 3),
                    'number': 1
                },
            ]
        ]
    ]
    print("List of Moves for the scenarios")
    print(target_engine.targets_to_moves(board=board, targets_scenarios_list=targets_scenarios_list))


def target_generation_test():
    board = __create_random_board(10, 10)
    print(board)

    all_attributions = target_engine.get_feasible_targets_turns(board, 'us')
    print(f"nodes number for us: {len(all_attributions)}")
    for attribution in all_attributions:
        check_targets(board, attribution)

    all_attributions = target_engine.get_feasible_targets_turns(board, 'them')
    print(f"nodes number for them: {len(all_attributions)}")
    for attribution in all_attributions:
        check_targets(board, attribution)


if __name__ == "__main__":
    target_generation_test()
    # ramdom_moves_test()
    # test_negatif()

    # esperance_tests()
    # print("esperance_tests done")

    # board_test_1()
    # print("board_test_1 done")

    # random_targets_test()
    # print("random_targets_test done")

    # random_target_test_2()
    # print("random_targets_test_2 done")

    # targets_to_move_test()
    # print("targets_to_move_test done")
