import numpy as np

import time
import xml.etree.ElementTree as ET

from models.cell import Cell
from models.board import Board
from strategies.target_strategy import TargetStrategy
from strategies.target_strategy_v2 import TargetStrategy2
from strategies.heuristics import distance_target_difference_heuristic
import cProfile


def loadMap(map_path):
	tree = ET.parse(map_path)
	root = tree.getroot()

	max_x, max_y = int(root.attrib['Columns']), int(root.attrib['Rows'])
	board = Board(max_x, max_y)

	for element in root.iter('Humans'):
		attribs = element.attrib
		board.update_cell2(Cell(int(attribs['X']), int(attribs['Y']), 'humans', int(attribs['Count'])))

	for element in root.iter('Werewolves'):
		attribs = element.attrib
		board.update_cell2(Cell(int(attribs['X']), int(attribs['Y']), 'us', int(attribs['Count'])))

	for element in root.iter('Vampires'):
		attribs = element.attrib
		board.update_cell2(Cell(int(attribs['X']), int(attribs['Y']), 'them', int(attribs['Count'])))

		return max_x, max_y, board

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

	strategy.next_moves(60)

def test2():

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

	strategy = TargetStrategy2(max_x, max_y, distance_target_difference_heuristic)
	strategy.current_board = board

	t0 = time.time()
	strategy.next_moves(2)
	print(f"time spent: {time.time() - t0}")


def test3():
	max_x, max_y, board = loadMap('test_maps/map_10_10_12.xml')
	strategy = TargetStrategy2(max_x, max_y, distance_target_difference_heuristic)
	strategy.current_board = board
	t0 = time.time()
	strategy.next_moves(2)
	print(f"time spent: {time.time() - t0}")

if __name__ == "__main__":  # python -m cProfile -s tottime speed_test.py
	test3()
