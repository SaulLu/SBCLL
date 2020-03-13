import numpy as np

from models.cell import Cell
from models.board import Board
from models.engine import Engine
from strategies.heuristics import naive_heuristic
from strategies.heuristics import distance_target_heuristic

def __create_random_board(max_x, max_y):
	board = Board(max_x, max_y)
	for _ in range(20):
		species = [None, 'us', 'them', 'humans']
		s = species[np.random.randint(len(species))]
		if s == None:
			number = 0
		else:
			number = np.random.randint(10)
		board.update_cell2(Cell(np.random.randint(max_x), np.random.randint(max_y), s, number))
	print(board)

def board_test_1():
	max_x = 5
	max_y = 5
	board = Board(max_x, max_y)
	engine = Engine()
	our_name = 'vampires'
	for i in range(5000):
		if np.random.random() > 0.5:
			species = [None, 'us', 'them', 'humans']
			s = species[np.random.randint(len(species))]
			if s == None:
				number = 0
			else:
				number = np.random.randint(10)
			board.update_cell2(Cell(np.random.randint(max_x), np.random.randint(max_y), s, number))
		else:
			species = [None, 'vampires', 'werewolves', 'humans']
			s = species[np.random.randint(len(species))]
			if s == None:
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

def distance_target_heuristic_test_1():
	board = __create_random_board(6,9)
	print(distance_target_heuristic(board))


def targets_test_1():
	engine = Engine()
	board = Board(5,5)

	board.update_cell((1,4), "humans", 2, "vampires")
	board.update_cell((4,4), "humans", 2, "vampires")
	board.update_cell((1,3), "wervolves", 1, "vampires")
	board.update_cell((3,3), "wervolves", 4, "vampires")
	board.update_cell((2,2), "vampires", 4, "vampires")

	for target_mov in engine.get_target_moves(board.get_cell(2,2), board):
		s = ""
		for t,n in target_mov:
			s = s + f" {t['coords']}, {t['creature']}, {t['number']} => {n};"
		print(s)


if __name__ == "__main__":
	#board_test_1()
	#print("board_test_1 done")

	#targets_test_1()
	#print("targets_test_1 done")

	#__create_random_board(5,8)
	#print("create_random_board done")

	distance_target_heuristic_test_1()
	print("distance_target_heuristic_test_1 done")