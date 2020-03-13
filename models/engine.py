import numpy as np
import itertools as iter
import math

from models.board import Board
from models.cell import Cell
from models.mov import Mov


class Engine():
    """Class doing any calculation required on a board
    """

    def __init__(self):
        pass

    #Add method to use in cell_output_if_attacked

    def apply_possible_board_many_moves(self, board, moves_list, attacker_species, method=None):
        """Method that applies moves to a board"""
        for move in moves_list:
            self.apply_possible_board_one_move(board, move, attacker_species, method=None)

    def apply_possible_board_one_move(self, board, move, attacker_species, output_species=None, output_qty=None):
        """Method that applies the result of one move to a board"""
        x_init = move.coord_init[0]
        y_init = move.coord_init[1]
        x_dest = move.coord_arriv[0]
        y_dest = move.coord_arriv[1]

        defender_cell = board.get_cell(x_dest, y_dest)

        if output_species==None:
            # Get new states by using random in real time if outputs not given
            output_winning_species, output_qty = self.cell_output_if_attacked(defender_cell, attacker_species, move.number_indiv, method)
        
        new_state_defender_cell = Cell(x_dest, y_dest, output_winning_species, output_qty)
        new_state_attacker_cell = Cell(x_init, y_init, attacker_species, board.get_cell(x_init, y_init).number - move.number_indiv)

        board.update_cell2(new_state_defender_cell)
        board.update_cell2(new_state_attacker_cell)

    def create_possible_board_many_moves(self, current_board, moves_list, attacker_species, method=None):
        """Method that generates a possible board for any given legal combination of moves"""
        return_board = current_board.deepcopy()
        self.apply_possible_board_many_moves(return_board, moves_list, attacker_species, method)
        return return_board

    def create_possible_board_one_move(self, current_board, move, attacker_species, method):
        """Method that generates a possible board for any given legal move"""
        new_possible_board = current_board.deepcopy()
        self.apply_possible_board_one_move(new_possible_board, move, attacker_species, method)
        return new_possible_board

    def get_all_possible_boards_many_moves(self,current_board, moves_list, attacker_species):
        
    
    def get_all_possible_boards_one_move(self,current_board, move, attacker_species, method):
        """Method that returns all the possible boards resulting from a move on a board and their probabilities"""
        all_possibilities = []
        possible_outputs = self.cell_outputs_if_attacked(defender_cell, attacker_species, move.number_indiv, method)
        for output in possible_outputs:
            new_board = current_board.deepcopy()
            new_board.apply_possible_board_one_move(current_board, move, output["winning_species"], output["output_qty"])
            all_possibilities.append((new_board, output["output_proba"]))
        return all_possibilities


    def cell_outputs_if_attacked(self, defender_cell, attacker_species, attacker_qty, method=None):
        """Method that gives the hypothetic output state of cell if it is under attack .
        
        Arguments:
            defender_cell {Cell} -- cell that is being attacked
            attacker_species {string} -- name of the creature attacking the cell
            attacker_qty {int}  -- number of attackers

        :returns
           a list of possible outputs
        """
        outputs = []
        if defender_cell.creature == "humans":
            if attacker_qty >= defender_cell.number:
                outputs.append({{"output_proba":1, "output_species": attacker_species, "output_qty": defender_cell.number + attacker_qty})
            else:
                if method = "esperance":
                    outputs = self._all_outputs_random_battle(defender_cell, attacker_species, attacker_qty)
                else:
                    outputs.append(self.__random_battle(defender_cell, attacker_species, attacker_qty))
                
        elif attacker_qty >= 1.5 * defender_cell.number:
            output = {"output_proba":1,"output_species": attacker_species, "output_qty": attacker_qty}
        else:
            if method = "esperance":
                outputs = self._all_outputs_random_battle(defender_cell, attacker_species, attacker_qty)
             else:
                outputs.append(self.__random_battle(defender_cell, attacker_species, attacker_qty))
        
        return outputs

    
    def _all_outputs_random_battle(self, defender_cell, attacker_species, attacker_qty):
        
         # 1. Calculate probability p that attackers win
        if attacker_qty == defender_cell.number:
            p = 0.5
        elif attacker_qty < defender_cell.number:
            p = attacker_qty / (2 * defender_cell.number)
        else:
            p = -0.5 + attacker_qty / defender_cell.number
        
        # 2. Get mean output of attackers survivors if attackers win
        esperance_attackers = 0
        for possible_number_survivors in range(1,attacker_qty+1):
            esperance_attackers += possible_number_survivors * get_probability(possible_number_survivors, attacker_qty, p)
        esperance_attackers = esperance_attackers*p

        # add mean nb of humans survivors if they are the defenders
        if defender_cell.creature == "humans":
            esperance_humans = 0
            for possible_number_survivors in range(1, defender_cell.number+1):
                esperance_humans += possible_number_survivors * get_probability(possible_number_survivors, defender_cell.number, p)
        esperance_attackers += esperance_humans

        # 3. Get mean output of defenders survivors if attackers lose
        esperance_defenders = 0
        for possible_number_survivors in range(1, defender_cell.number+1):
            esperance_defenders += possible_number_survivors * get_probability(possible_number_survivors, defender_cell.number, 1-p)

        return [{"output_proba":p, "output_species": attacker_species, "output_qty":esperance_attackers},
        {"output_proba":1-p, "output_species": defender_cell.creature, "output_qty":esperance_defenders}]

    def get_probability(possible_number_survivors, initial_total_number, p):
        """Calculate the binomial probability of having possible_number_survivors"""
        return binom(initial_total_number, possible_number_survivors) * p**(possible_number_survivors) * (1-p)**(initial_total_number-possible_number_survivors)


    def binom(n, k):
        return math.factorial(n) // math.factorial(k) // math.factorial(n - k)
    
    def __random_battle(self, defender_cell, attacker_species, attacker_qty):
        """Private method that simulates a random battle.
            
            Arguments:
                defender_cell {Cell} -- cell that is being attacked
                attacker_species {string} -- name of the creature attacking the cell
                attacker_qty {int}  -- number of attackers
            
        
            Returns:
                dict{string: <string,int>} -- return the type of the winner species in the cell and their quantity
        """
        # 1. Calculate probability p that attackers win
        if attacker_qty == defender_cell.number:
            p = 0.5
        elif attacker_qty < defender_cell.number:
            p = attacker_qty / (2 * defender_cell.number)
        else:
            p = -0.5 + attacker_qty / defender_cell.number

        # 2. Determine winner
        winner_species = np.random.choice([attacker_species, defender_cell.creature], 1, p=[p, 1 - p])[0]

        # 3. Count winner survivors
        if winner_species == attacker_species:
            # Attackers win
            number_winners_survivors = self.__get_total_survivors(attacker_qty, p)
            if defender_cell.creature == "humans":
                number_humans_survivors = self.__get_total_survivors(defender_cell.number, p)
                number_winners_survivors += number_humans_survivors
        else:
            # Defenders win
            number_winners_survivors = self.__get_total_survivors(defender_cell.number, 1 - p)

        return {"output_proba":None, "output_species": winner_species, "output_qty": number_winners_survivors}

    def __get_total_survivors(self, initial_quantity, proba_to_survive):
        """Private method that gets the number of survivors of a given quantity of creatures according to a certain probability to survive.
        
        Arguments:
            initial_quantity {int} -- initial numbers of creatures
            proba_to_survive {float}  -- probability to survive
        """
        total_survivors = 0
        for _ in range(initial_quantity):
            total_survivors += np.random.choice([1, 0], 1, p=[proba_to_survive, 1 - proba_to_survive])[0]
        return total_survivors

    def adjacent_cells(self, i_coord, j_coord, board):
        """Method that returns the index of the existing adjacent cells for a given cell.
        
        Arguments:
            i_coord {int} -- index of row
            j_coord {int} -- index of column
        """

        adjacents = []
        for x, y in [(i_coord + i, j_coord + j) for i in (-1, 0, 1) for j in (-1, 0, 1) if i != 0 or j != 0]:
            if ((x >= 0) and (x < board.max_x) and (y >= 0) and (y < board.max_y)):
                adjacents.append((x, y))

        return adjacents

    def get_targetable_cells(self, i_coord, j_coord, creature, board):
        return [adj for adj in self.adjacent_cells(i_coord, j_coord, board) if board.grid[adj[0]][adj[1]].creature != creature ]

    def get_cell_moves(self, cell, board):
        """Lists all the ways to divide (or not) the current group and move the members to adjacent cells.
        Returns all possibilities, including not doing anything.
        
        Arguments:
            cell {Cell} -- the instance of Cell from which we want to know possible moves
            board {Board} -- the instance of Board
        
        Returns:
            [array] -- an array containing arrays of the combination of possible Mov instances
        """
        possible_moves = []

        # current cell and adjacent cells
        possible_cells = [(cell.x, cell.y)]
        for adj_cell in self.adjacent_cells(cell.x, cell.y, board):
            possible_cells.append(adj_cell)
        

        # all combinations of the integers from 0 to the number of creatures included,
        # contains all possible ways of diving the members present on the cell in different groups
        all_div = iter.combinations_with_replacement(range(cell.number + 1), len(possible_cells))

        for div in all_div:
            if sum(div) == cell.number:  # possible division, with the correct number of creatures
                permutations = iter.permutations(div)
                permutations = set(permutations)  # removes duplicates
                for perm in permutations:
                    move = []
                    for i in range(len(perm)):                        
                        if (perm[i]>0):
                            if ((cell.x,cell.y) != possible_cells[i]):
                                mov = Mov((cell.x,cell.y), perm[i], possible_cells[i])
                                move.append(mov) # initial coordinates are that of the considered cell
                    if len(move)>0:
                        possible_moves.append(move)
                    
        return possible_moves

    def get_possible_turns(self, board, creature_name):
        """Computes all possible moves for a given board and given creature
        
        Arguments:
            board {Board} -- the instance of Board to consider
            creature_name {string} -- the creature to be considered, "us" or "them"
        
        Returns:
            [array] -- an array containing array of Mov instances : each array represents a board
                obtainable from considered board after movs have been played 
        """
        moves = []
        # find all cells with correct creatures
        cells=[]
        for row in board.grid:
            for cell in row:
                if cell.creature == creature_name:
                    cells.append(cell)

        # list all possible moves for each of the cells
        for cell in cells:
            moves_cell = []
            for m in self.get_cell_moves(cell, board):
                moves_cell.append(m)
            moves.append(moves_cell)

            # combine all different moves for each cell together
        combinations = iter.product(*moves)

        # identify the move where nothing changes and take it out    
        result = []
        for c in combinations:
            flatten_c = []
            for item in c:
                if isinstance(item, list):
                    for item_bis in item:
                        flatten_c.append(item_bis)
                else :
                    flatten_c.append(item)

            departurs = set(x.coord_init for x in flatten_c)
            arrivals = set(x.coord_arriv for x in flatten_c)
            if len(list(departurs & arrivals)) == 0:
                result.append(flatten_c)    
            
        return result

    def get_random_turn(self, board, creature_name):
        """randomly select a turn for a given board and given creature
        
        Arguments:
            board {Board} -- the instance of Board to consider
            creature_name {string} -- the creature to be considered, "us" or "them"
        
        Returns:
            [Mov()] -- an array of Mov instances : it represents a board
                obtainable from considered board after movs have been played 
        """
        cells=[]
        for row in board.grid:
            for cell in row:
                if cell.creature == creature_name:
                    cells.append(cell)

        moves = []
        while len(moves) == 0:
            for cell in cells:
                targets = self.get_targetable_cells(cell.x, cell.y, creature_name, board)
                if len(targets):
                    for i in range(cell.number):
                        if np.random.random() > 0.5: #will move!
                            target_i = np.random.randint(0,len(targets))
                            moves.append(Mov((cell.x, cell.y), 1, targets[target_i]))
        return moves



    def count_creatures(self, board):
        """Method to count the number of each creature (us, them, humans). 
        
        Arguments:        
            board {Board} -- an instance of Board class to evaluate
        
        Returns:
            (int, int, int) -- the number of each creature in that order :(us, them, humans)
        """

        number_of_us = 0
        number_of_them = 0
        number_of_humans = 0

        for i in range(board.max_x):
            for j in range(board.max_y):
                if board.grid[i][j].creature == "us":
                    number_of_us += board.grid[i][j].number
                elif board.grid[i][j].creature == "them":
                    number_of_them += board.grid[i][j].number
                elif board.grid[i][j].creature == "humans":
                    number_of_humans += board.grid[i][j].number

        return number_of_us, number_of_them, number_of_humans



    def __recursive_target_attribution(self, prev_attributions, remaining_creatures, avalaible_targets):
        n_avalaible_targets = len(avalaible_targets)
        if remaining_creatures == 0 or n_avalaible_targets == 0:
            return [prev_attributions + [(target, 0) for target in avalaible_targets]]
        else:
            all_attributions = []
            target = avalaible_targets[0]

            new_attribution = prev_attributions + [(target, 0)]
            all_attributions = all_attributions + self.__recursive_target_attribution(new_attribution, remaining_creatures, avalaible_targets[1:])
            if target['min_takeover'] <= remaining_creatures:
                for i in range(target['min_takeover'], remaining_creatures + 1):
                    new_attribution = prev_attributions + [(target, i)]
                    all_attributions = all_attributions + self.__recursive_target_attribution(new_attribution, remaining_creatures - i, avalaible_targets[1:])
                
            return all_attributions


    def get_target_moves(self, cell, board):
        min_takeover_factor = {'them':1.5, 'humans':1}
        creature = cell.creature
        targets = []
        for s in board.creatures_list:
            if s != creature:
                for cell_coords in board.creatures_list[s]:
                    number = board.creatures_list[s][cell_coords]
                    min_takeover = int(math.ceil(min_takeover_factor[s] * number))
                    targets.append({'coords': cell_coords, 'number':number, 'creature':s, 'min_takeover': min_takeover })

        global_min = min([t['min_takeover'] for t in targets])
        all_attributions = self.__recursive_target_attribution([], cell.number, targets)

        return all_attributions



