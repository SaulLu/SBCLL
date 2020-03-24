import numpy as np

from models.cell import Cell
from models.board import Board
import models.engine as engine
import models.target_engine as target_engine
from strategies.heuristics import naive_heuristic
from strategies.heuristics import distance_target_heuristic
from strategies.heuristics import distance_target_difference_heuristic
from models.mov import Mov


def print_heuristics(board):
    print(board)
    print(f"naive:{naive_heuristic(board)}")
    print(f"distance_target_heuristic:{distance_target_heuristic(board)}")
    print(f"distance_target_difference_heuristic:{distance_target_difference_heuristic(board)}")


def test1():
    """
    flee the enemy and go to the humans
    :return:
    """
    board = Board(5, 5)

    board.update_cell2(Cell(2, 2, 'us', 4))
    board.update_cell2(Cell(0, 4, 'them', 8))
    board.update_cell2(Cell(4, 2, 'humans', 1))

    print_heuristics(board)

    moves = [Mov((2, 2), 4, (3, 2))]
    board2 = engine.create_possible_boards_many_moves(board, moves, 'us')[0][0]

    print(print_heuristics(board2))

    moves = [Mov((3, 2), 4, (4, 2))]
    board3 = engine.create_possible_boards_many_moves(board2, moves, 'us')[0][0]

    print(print_heuristics(board3))


def test2():
    """
    every one, move!
    :return:
    """
    board = Board(5, 5)

    board.update_cell2(Cell(2, 2, 'them', 4))
    board.update_cell2(Cell(0, 4, 'us', 8))
    board.update_cell2(Cell(4, 2, 'humans', 1))

    print_heuristics(board)

    moves = [Mov((0, 4), 7, (1, 3))]
    board2 = engine.create_possible_boards_many_moves(board, moves, 'us')[0][0]

    print(print_heuristics(board2))

    moves = [Mov((0, 4), 8, (1, 3))]
    board3 = engine.create_possible_boards_many_moves(board, moves, 'us')[0][0]

    print(print_heuristics(board3))


def test3():
    board = Board(6, 5)

    board.update_cell2(Cell(3, 0, 'them', 4))
    board.update_cell2(Cell(0, 2, 'us', 8))
    board.update_cell2(Cell(5, 0, 'humans', 2))
    board.update_cell2(Cell(5, 2, 'humans', 1))
    board.update_cell2(Cell(5, 4, 'humans', 2))

    print_heuristics(board)

    moves = [Mov((0, 2), 7, (1, 1))]
    board2 = engine.create_possible_boards_many_moves(board, moves, 'us')[0][0]

    print(print_heuristics(board2))

    moves = [Mov((0, 2), 8, (1, 1))]
    board3 = engine.create_possible_boards_many_moves(board, moves, 'us')[0][0]

    print(print_heuristics(board3))


if __name__ == "__main__":
    test3()
