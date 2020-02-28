from models.cell import Cell
import numpy as np


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
        self.grid = np.asarray([[Cell(x,y) for y in range(self.max_y) ] for x in range(self.max_x)])

    def update_cell(self, coords, species, number, our_name):
        """Method to update a given cell.

        Arguments:
            coords {(int, int)} -- tuple indicating the number of row and the number of columns
            species {string} -- name of the creature present in this cell
            number {int} -- number of creatures present in this cell
            our_name {string} -- name of the species played by us
        """
        cell_to_update = self.grid[coords[0]][coords[1]]
        # Anonymization
        if species == 'humans':
            species_anonymous = 'humans'
        elif species == our_name:
            species_anonymous = 'us'
        else :
            species_anonymous = 'them'
        cell_to_update.update(species_anonymous, number)

    def update_cell_without_name(self, cell):
        """Method to update a given cell.

                Arguments:
                    the new cell
                """
        cell_to_update = self.grid[cell.x][cell.y]
        # Anonymization
        cell_to_update.update(cell.creature, cell.number)

    def get_cell(self, x, y):
        """This method returns a cell element for a given x and y"""
        return self.grid[x][y]
