import numpy as np
import itertools as iter 
from models.mov import Mov 

class Engine():
    """Class doing any calculation required on a board
    """
    def __init__(self):
        pass

    def get_all_moves(self, board, cell):
        """Method that gives all the available moves for a given cell

        Arguments:
            cell {Cell} -- origin cell"""

        coord_init = (cell.x, cell.y)
        number_creature = cell.number
        possible_moves = []
        return_moves = []
        "Ramener mov de client au bon endroit pour que ce soit propre ensuite"
        for i in range(-1, 1):
            for j in range(-1, 1):
                coord_dest = (cell.x - i, cell.y - j)
                mov = (coord_init, 1, coord_dest)
                if self.is_legal(board, mov):
                    possible_moves.append(mov)

        for combin_moves in itertools.chain(*(itertools.combinations(possible_moves, long) for long in range(1, len(possible_moves)))):
            for p in self.recursiv_attribution([], number_creature, combin_moves):
                return_moves.append(p)

        print(return_moves)
        return return_moves

    def is_legal(self, board, mov):
        y_max = board.n_rows
        x_max = board.n_columns
        if mov.coord_arriv == mov.coord_init:
            return False
        if mov.coord_arriv[0] < 0 or mov.coord_arriv[0] > y_max:
            return False
        if mov.coord_arriv[1] < 0 or mov.coord_arriv[1] > x_max:
            return False
        return True

    def recursiv_attribution(self, prev_attributions, remaining_creatures, avalaible_moves):
        if remaining_creatures == 0:
            return list(prev_attributions) + len(avalaible_moves) * [0]
        elif len(avalaible_moves) == 0:
            return [list(prev_attributions)]
        else:
            all_attributions = []
            move = avalaible_moves[0]
            min_attribution = 0
            if len(avalaible_moves) == 1 and sum([p[1] for p in prev_attributions]) == 0:
                min_attribution = 1
            for i in range(min_attribution, remaining_creatures):
                new_attribution = list(prev_attributions) + [(move, i)]
                all_attributions = all_attributions + f(new_attribution, remaining_creatures - i, avalaible_moves[1:])
            return all_attributions


    def cell_output_if_attacked(self, defender_cell, attacker_species, attacker_qty):
        """Method that gives the hypothetic output state of cell if it is under attack .
        
        Arguments:
            defender_cell {Cell} -- cell that is being attacked
            attacker_species {string} -- name of the creature attacking the cell
            attacker_qty {int}  -- number of attackers  
        """
        if defender_cell.creature == "humans":
            if attacker_qty >= defender_cell.number:
                output = {"creature": attacker_species, "number": defender_cell.number + attacker_qty}
            else:
                output = self.__random_battle(defender_cell, attacker_species,attacker_qty) 
        elif attacker_qty >= 1.5*defender_cell.number:
            output = {"creature":attacker_species, "number": attacker_qty}
        else:
            output = self.__random_battle(defender_cell, attacker_species,attacker_qty)
        return output


    def __random_battle(self, defender_cell, attacker_species, attacker_qty):
            """Private method that simulates a random battle.
            
            Arguments:
                defender_cell {Cell} -- cell that is being attacked
                attacker_species {string} -- name of the creature attacking the cell
                attacker_qty {int}  -- number of attackers
            """ 
            # 1. Calculate probability p
            if attacker_qty == defender_cell.number :
                p = 0.5
            elif attacker_qty < defender_cell.number:
                p = attacker_qty / (2*defender_cell.number)
            else:
                p= -0.5 + attacker_qty/defender_cell.number
            
            # 2. Determine winner
            winner_species = np.random.choice([attacker_species, defender_cell.creature], 1, p=[p, 1-p])[0]
        
            # 3. Count winner survivors
            if winner_species==attacker_species:
                # Attackers win
                number_winners_survivors =  self.__get_total_survivors(attacker_species, p)
                if defender_cell.species == "humans":
                    number_humans_survivors = self.__get_total_survivors(defender_cell.number, p)
                    number_winners_survivors += number_humans_survivors
            else:
                # Defenders win
                number_winners_survivors =  self.__get_total_survivors(defender_cell.number, 1-p)
            
            return {"creature":winner_species, "number": number_winners_survivors}

    def __get_total_survivors(self, initial_quantity, proba_to_survive):
        """Private method that gets the number of survivors of a given quantity of creatures according to a certain probability to survive.
        
        Arguments:
            initial_quantity {int} -- initial numbers of creatures
            proba_to_survive {float}  -- probability to survive
        """
        total_survivors = 0
        for _ in range(initial_quantity):
            total_survivors += np.random.choice([1, 0], 1, p=[proba_to_survive, 1-proba_to_survive])[0]
        return total_survivors
    
    def adjacent_cells(self, i_coord, j_coord, board):
        """Method that returns the index of the existing adjacent cells for a given cell.
        
        Arguments:
            i_coord {int} -- index of row
            j_coord {int} -- index of column
        """
        assert(i_coord>=0 and i_coord<board.max_x,"Row index out of grid")
        assert(((j_coord>=0) and (j_coord<board.max_y)),"Column index out of grid")

        adjacent = []
        for x,y in [(i_coord+i,j_coord+j) for i in (-1,0,1) for j in (-1,0,1) if i != 0 or j != 0]:
            if ((x>=0) and (x<board.max_x) and (y>=0) and (y<board.max_y)):
                adjacent.append((x,y))
        
        return adjacent 

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
        for cell in self.adjacent_cells(cell.x, cell.y, board):
            possible_cells.append(cell)
        
        # all combinations of the integers from 0 to the number of creatures included,
        # contains all possible ways of diving the members present on the cell in different groups
        all_div = iter.combinations_with_replacement(range(cell.number+1), len(possible_cells))

        for div in all_div: 
            if sum(div) == cell.number: # possible division, with the correct number of creatures
                permutations = iter.permutations(div)  
                permutations = set(permutations) # removes duplicates
                for perm in permutations:
                    move = []
                    for i in range(len(perm)):                        
                        if (perm[i]>0):
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
        for row in board:
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
            only_one_move = list(filter(lambda x : len(x) == 1, c)) # combination of moves where the group is not divided
            nothing_changes = list(filter(lambda x: x[0].coord_init == x[0].coord_arriv, only_one_move)) # combination of moves where origin = destination for each : invalid 
            if not(len(nothing_changes) == len(cells)):
                flatten_c = []
                for item in c:
                    if isinstance(item, list):
                        for item_bis in item:
                            flatten_c.append(item_bis)
                    else :
                        flatten_c.append(item)
                result.append(flatten_c)    
            
        return result
        
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
                if board[i][j].creature == "us":
                    number_of_us += 1
                elif board[i][j].creature == "them":
                    number_of_them += 1
                elif board[i][j].creature == "humans":
                    number_of_humans += 1
        
        return number_of_us, number_of_them, number_of_humans
