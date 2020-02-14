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

    def update_cell(self, coords, species, number):
        """Method to update a given cell.
        
        Arguments:
            coords {(int, int)} -- tuple indicating the number of row and the number of columns
            species {string} -- name of the creature present in this cell
            number {int} -- number of creatures present in this cell
        """
        cell_to_update = self.grid[coords[0]][coords[1]]
        cell_to_update.update(species, number)

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

class Player():
    """Class 
    """
    def __init__(self):
        """ Constructor for player
        """
        self.our_name = None
        self.opponent_name = None
        self.current_board = None
        self.is_my_turn = None
        self.first_position = None
        self.receive_our_position = False
        self.receive_all_positions = False
    
    def init_connection(self, ip, port):
        # call function to init the connection
        pass

    def init_board(self, n_rows, n_columns):
        """Function to init the board when SET is received
        Arguments:
        n_rows {int} -- number of rows
        n_columns {int} -- number of columns
        """
        self.current_board = Board(n_rows, n_columns)

    def init_humans(self, humans_coords):
        #useless apiori
        pass    
    def init_home(self, x, y):
        """Function to store our info when HME is received
        
        Arguments:
            x {int} -- row
            y {[type]} -- column
        """
        self.first_position = (x,y)
        if self.receive_all_positions:
            #appeler fonction pour definition our_name and opponent_name
            #appeler fonction pour changer les noms sur la board
            pass

    def init_update(self, list_updates):
        """Function to update the board when MAP or UPD is received
        
        Arguments:
            list_updates {list(dict)} -- list of dictionaries. Each dictionary contains information \
                in a cell that should be changed. The format used for each dictionary is \
                    {'coords': (int, int), 'species': string, 'number': int}
        """
        for update_one_cell in list_updates:
            # update_one_cell format is like {'coords': (2, 2), 'species': 'humans', 'number': 1}
            self.current_board.update_cell(update_one_cell)
    
        if self.receive_our_position:
            #appeler fonction pour changer les noms sur la board
            pass

    def init_game(self, ):
        """Initialise the game with the info received by the command 
        """
        self.our_name = our_species_name
        assert((self.our_name in ["werewolves", "vampires"]), 'Not allowed creature name')
        self.opponent_name = "werewolves" if self.our_name == "vampires" else "vampires"
        self.is_my_turn = 
        self.current_board.update_board(#dict with info)