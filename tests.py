import numpy as np

from models.cell import Cell
from models.board import Board
from models.engine import Engine
from strategies.heuristics import naive_heuristic

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

if __name__ == "__main__":
	board_test_1()
	print("board_test_1 done")