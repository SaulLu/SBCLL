
from strategies.abstract_strategy import Strategy
import numpy as np 
import time

class Squad():
    def __init__(self, creature, number):
        self.creature = creature
        self.number = number
        self.target = None


class TargetWalkStrategy(Strategy):
    def __init__(self, max_x, max_y, heuristic):
        super().__init__(max_x, max_y, heuristic)
        #super().__init__(new_attribute_1, new_attribute_2):

    def next_moves(self):
        t0 = time.time()

        all_possible_turns = self.engine.get_possible_turns(self.current_board, 'us')
        scoring = [{'n_walks':0, 'sum':0} for i in range(len(all_possible_turns))]

        timeout = 8
        max_step = 5
        count = 0
        while time.time() - t0  < timeout:
            random_turn_index = np.random.randint(0,len(all_possible_turns))
            new_board = self.engine.create_possible_board_many_moves(self.current_board, all_possible_turns[random_turn_index], 'us', None)
            score = self.targetWalk(new_board, 'them', max_step)
            scoring[random_turn_index]['n_walks'] += 1
            scoring[random_turn_index]['sum'] += score
            count += 1

        print(f"\nI did {count} walks, amongs {len(all_possible_turns)} first turns")

        

        #scoring_computed = [(s['sum'] / s['n_walks'] if s['n_walks'] else -np.inf,i)  for i,s in enumerate(scoring)]
        #scoring_computed.sort(reverse = True)
        #for i in range(3):
        #	print(f"score: {scoring_computed[i][0]}, moves: {all_possible_turns[scoring_computed[i][1]]}")
        #best_score, chosen_turn_index = scoring_computed[0]
        
        scoring_computed = [s['sum'] / s['n_walks'] if s['n_walks'] else -np.inf  for s in scoring]
        chosen_turn_index = np.argmax(scoring_computed)
        best_score = scoring_computed[chosen_turn_index]
        print(f"best_score: {best_score}")

        return all_possible_turns[chosen_turn_index]

    def targetWalk(self, board, next_species, step_left):
        if step_left == 0:
            return self.heuristic(self.engine, board)
        else:
            n_us, n_them, n_h = self.engine.count_creatures(board)
            if n_us * n_them:
                random_turn = self.engine.get_random_turn(board, next_species)
                reverse_species ={'us':'them','them':'us'}

                self.engine.apply_possible_board_many_moves(board, random_turn, next_species, None)
                return self.randomWalk(board, reverse_species[next_species], step_left - 1)
            else:
                return self.heuristic(self.engine, board)