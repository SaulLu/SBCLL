class Board():
    """Class modelizing the board
    """
    def __init__(self):
        """Constructor for Board
        """
        self.n_rows = 0
        self.n_columns = 0
        self.grid = [[Cell() for col in range(self.n_columns) ] for lig in range(self.n_rows)]

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
    def __init__(self, our_species_name):
        """ Constructor for General game information
        
        Arguments:
            our_species_name {string} -- "werewolves" or "vampires"
        """
        self.our_name = our_species_name
        assert((self.our_name in ["werewolves", "vampires"]), 'Not allowed creature name')
        self.opponent_name = "werewolves" if self.our_name == "vampires" else "vampires"