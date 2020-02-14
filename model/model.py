import numpy as np

class Board:
    """Class modelizing the board
    """
    def __init__(self, number_rows, number_columns):
        """Constructor for Board
        
        Arguments:
            number_rows {[type]} -- number of rows wanted
            number_columns {[type]} -- number of columns wanted
        """
        self.n_rows = number_rows
        self.n_columns = number_rows
        self.grid = [[Cell() for col in range(self.n_columns) ] for lig in range(self.n_rows)]

    def update_board(self, dic):
        """update the grid with the info received from the server
        
        Arguments:
            dic {dict} -- keys (x,y) -> dict -> keys species and number
        """
        for coord in dic:
            self.grid[coord].creature = dic[coord]['species']
            self.grid[coord].number = dic[coord]['number']

    def update_cell(self, i_coord, j_coord, creature_name, number_creatures):
        """Method to update a given cell.
        
        Arguments:
            i_coord {int} -- index of row
            j_coord {int} -- index of column
            creature_name {string} -- name of the creature present in this cell
            number_creature {int} -- number of creatures present in this cell
        """

        cell_to_update = self.grid[i_coord][j_coord]
        cell_to_update.update(creature_name, number_creatures)

    def adjacent_cells(self, i_coord, j_coord):
        """Method that returns the index of the existing adjacent cells for a given cell.
        
        Arguments:
            i_coord {int} -- index of row
            j_coord {int} -- index of column
        """
        assert(i_coord>=0 and i_coord<self.n_rows,"Row index out of grid")
        assert(((j_coord>=0)and(j_coord<self.n_columns)),"Column index out of grid")

        adjacent = []
        for x,y in [(i_coord+i,j_coord+j) for i in (-1,0,1) for j in (-1,0,1) if i != 0 or j != 0]:
            if ((x>=0) and (x<self.n_rows) and (y>=0) and (y<self.n_columns)):
                adjacent.append((x,y))
        
        return adjacent          

    
    def naive_heuristic(self, creature_name):
        """Method to measure the advantage of given creature (werewolves or vampires) for the board. 
        Counts the difference between the number of werewolves and that of vampires, or vice-versa.
        
        Arguments:
            creature_name {string} -- name of the creature to consider, "werewolves" or "vampires"
        """
        assert((creature_name in ["werewolves", "vampires"]), 'Not allowed creature name')

        number_of_vampires = 0
        number_of_werewolves = 0

        for i in range(self.n_rows):
            for j in range(self.n_columns):
                if self.grid[i][j].creature == "vampires":
                    number_of_vampires += 1
                elif self.grid[i][j].creature == "werewolves":
                    number_of_werewolves += 1
        
        if creature_name == "vampires":
            return number_of_vampires - number_of_werewolves
        else: 
            return number_of_werewolves - number_of_vampires
        

class Cell:
    """Class for the content of a cell
    """
    def __init__(self):
        """Constructor for Cell
        """
        self.creature = None
        self.number = 0
        creatures = [None, "humans", "werewolves", "vampires"]
        assert((self.creature in creatures), 'Not allowed creature')
        
    def update(self, creature_name, number_creatures):
        """Method to update the cell.
        
        Arguments:
            creature_name {string} -- name of the creature present in this cell
            number_creature {int} -- number of creatures present in this cell
        """

        self.creature = creature_name
        self.number = number_creatures
    
    def output_if_attacked(self, attacker_species, attacker_qty):
        """Method that gives the hypothetic output state of the cell if it is under attack .
        
        Arguments:
            attacker_species {string} -- name of the creature attacking the cell
            attacker_qty {int}  -- number of attackers  
        """  
        if self.creature == "humans":
            if attacker_qty >= self.number :
                output = {"creature":attacker_species, "number": self.number + attacker_qty}
            else:
                output = __random_battle() 
        elif attacker_qty >= 1.5*self.number:
            output = {"creature":attacker_species, "number": attacker_qty}
        else:
            output = __random_battle()
        return output
    
    def __random_battle(attacker_species, attacker_qty, defender_species, defender_qty):
        """Private method that simulates a random battle.
        
        Arguments:
            attacker_species {string} -- name of the creature attacking the cell
            attacker_qty {int}  -- number of attackers
            defender_species {string} -- name of the creature attacking the cell
            defender_qty {int}  -- number of attackers 
        """ 
        # 1. Calculate probability p
        if attacker_qty = defender_qty :
            p = 0.5
        elif attacker_qty < defender_qty:
            p = attacker_qty / (2*defender_qty)
        else:
            p= -0.5 + attacker_qty/defender_qty
        
        # 2. Determine winner
        winner_species = np.random.choice([attacker_species, defender_species], 1, p=[p, 1-p])[0]
       
        # 3. Count winner survivors
        if winner_species==attacker_species:
            # Attackers win
            number_winners_survivors =  __get_total_survivors(attacker_species, p)
            if defender_species == "humans":
                number_humans_survivors = __get_total_survivors(defender_qty, p)
                number_winners_survivors += number_humans_survivors
        else:
            # Defenders win
            number_winners_survivors =  __get_total_survivors(defender_qty, 1-p)
        
        return {"creature":winner_species, "number": number_winners_survivors}

    def __get_total_survivors(initial_quantity, proba_to_survive):
        """Private method that gets the number of survivors of a given quantity of creatures according to a certain probability to survive.
        
        Arguments:
            initial_quantity {int} -- initial numbers of creatures
            proba_to_survive {float}  -- probability to survive
        """ 
        total_survivors = 0
            for i in range(initial_quantity):
                total_survivors += np.random.choice([1, 0], 1, p=[proba_to_survive, 1-proba_to_survive])[0]
        return total_survivors
        


class GameInfo:
    """Class for general game information
    """
    def __init__(self, our_species_name, n_rows, n_columns):
        """ Constructor for General game information
        
        Arguments:
            our_species_name {string} -- "werewolves" or "vampires"
        """
        self.our_name = our_species_name
        assert((self.our_name in ["werewolves", "vampires"]), 'Not allowed creature name')
        self.opponent_name = "werewolves" if self.our_name == "vampires" else "vampires"
        self.board = Board(n_rows, n_columns)
