import numpy as np

from models.cell import Cell
from models.board import Board
import models.engine as engine
import models.target_engine as target_engine


def board_test_1():
    max_x = 5
    max_y = 5
    board = Board(max_x, max_y)
    our_name = 'vampires'
    for i in range(5000):
        if np.random.random() > 0.5:
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


if __name__ == "__main__":
    board_test_1()
    print("board_test_1 done")

    random_targets_test()
    print("random_targets_test done")
