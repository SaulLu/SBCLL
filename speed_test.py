import numpy as np

from models.cell import Cell
from models.board import Board
from strategies.target_strategy import TargetStrategy
from strategies.heuristics import distance_target_difference_heuristic
import cProfile


def test1():

	max_x, max_y = 8, 8
	board = Board(max_x, max_y)

	board.update_cell2(Cell(0, 2, 'us', 4))
	board.update_cell2(Cell(1, 2, 'us', 2))
	board.update_cell2(Cell(2, 2, 'us', 4))
	board.update_cell2(Cell(0, 4, 'them', 8))
	board.update_cell2(Cell(0, 0, 'humans', 2))
	board.update_cell2(Cell(4, 2, 'humans', 1))
	board.update_cell2(Cell(4, 4, 'humans', 1))
	board.update_cell2(Cell(7, 7, 'humans', 1))
	board.update_cell2(Cell(3, 3, 'them', 1))
	board.update_cell2(Cell(6, 7, 'them', 2))

	strategy = TargetStrategy(max_x, max_y, distance_target_difference_heuristic)
	strategy.current_board = board

	strategy.next_moves(9.5)


if __name__ == "__main__":  # python -m cProfile -s tottime speed_test.py

	test1()