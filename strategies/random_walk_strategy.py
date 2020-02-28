
from strategies.abstract_strategy import Strategy
import numpy as np 
import time
import copy

class RandomWalkStrategy(Strategy):
    def __init__(self, max_x, max_y, heuristic):
        super().__init__(max_x, max_y, heuristic)
        #super().__init__(new_attribute_1, new_attribute_2):

    def next_moves(self):
        t0 = time.time()

        all_possible_turns = self.engine.get_possible_turns(self.current_board, 'us')
        scoring = {i:{'n_walks':0, 'sum':0} for i in range(len(all_possible_turns))}

        timeout = 5
        max_step = 100
        while time.time() - t0  < timeout:
            random_turn_index = np.random.randint(0,len(all_possible_turns))
            new_board = self.engine.create_possible_board_many_moves(self.current_board, all_possible_turns[random_turn_index], 'us', None)
            score = self.randomWalk(new_board, 'them', max_step)
            scoring[random_turn_index]['n_walks'] += 1
            scoring[random_turn_index]['sum'] += score


        chosen_turn_index = np.argmax([s['sum'] / s['n_walks'] if s['n_walks'] else -np.inf for s in scoring])
        return all_possible_turns[chosen_turn_index]

    def randomWalk(self, board, next_species, step_left):
        if step_left == 0:
            return self.heuristic(self.engine, board)
        else:
            all_possible_turns = self.engine.get_possible_turns(board, next_species)
            random_turn = all_possible_turns[np.random.randint(0,len(all_possible_turns))]

            reverse_species ={'us':'them','them':'us'}

            new_board = self.engine.create_possible_board_many_moves(board, random_turn, next_species, None)
            return self.randomWalk(new_board, reverse_species[next_species], step_left - 1)