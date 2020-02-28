from models.cell import Cell

class Board:
    """Class modelizing the board
    """
    def __init__(self, max_x, max_y):
        """Constructor for Board
        
        Arguments:
            max_x {int} -- number of columns wanted
            max_y {int} -- number of rows wanted
        """
        self.max_x = max_x
        self.max_y = max_y
        self.grid = [[Cell(x,y) for y in range(self.max_y) ] for x in range(self.max_x)]

    def update_cell(self, coords, species, number, our_name):
        """Method to update a given cell.
        
        Arguments:
            coords {(int, int)} -- tuple indicating the number of row and the number of columns
            species {string} -- name of the creature present in this cell
            number {int} -- number of creatures present in this cell
            our_name {string} -- name of the species played by us
        """
        print(coords, species, number, our_name)
        cell_to_update = self.grid[coords[0]][coords[1]]
        # Anonymization
        species_anonymous = 'us' if species == our_name else 'them'
        cell_to_update.update(species_anonymous, number)          
