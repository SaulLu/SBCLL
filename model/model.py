class Board():
    """Class modelizing the board
    """
    def __init__(self, n_rows, n_columns):
        """Constructor for Board
        """
        self.n_rows = 0
        self.n_columns = 0
        self.grid = [[Cell() for col in range(self.n_columns) ] for lig in range(self.n_rows)]

    def update_board(self, dic):
        """update the grid with the info received from the server
        
        Arguments:
            dic {dict} -- keys (x,y) -> dict -> keys species and number
        """
        for coord in dic:
            self.grid[coord].creature = dic[coord]['species']
            self.grid[coord].number = dic[coord]['number']

class Cell():
    """Class for the content of a cell
    """
    def __init__(self):
        """Constructor for Cell
        """
        self.creature = None
        self.number = 0
        creatures = [None, "humans", "werewolves", "vampires"]
        assert((self.creature in creatures), 'Not allowed creature')

class GameInfo():
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