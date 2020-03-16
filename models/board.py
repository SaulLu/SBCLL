from __future__ import annotations
import numpy as np


from models.cell import Cell


class Board:
    """Class modelizing the board
    """

    def __init__(self, max_x: int, max_y: int):
        """Constructor for Board
        
        Arguments:
            max_x {int} -- number of columns wanted
            max_y {int} -- number of rows wanted
        """
        self.max_x = max_x
        self.max_y = max_y
        self.grid = np.asarray([[Cell(x, y) for y in range(self.max_y)] for x in range(self.max_x)])
        self.creatures_list = {'us': {}, 'them': {}, 'humans': {}}

    def update_cell(self, coordinate, species, number, our_name):
        """Method to update a given cell.

        Arguments:
            coords {(int, int)} -- tuple indicating the number of row and the number of columns
            species {string} -- name of the creature present in this cell
            number {int} -- number of creatures present in this cell
            our_name {string} -- name of the species played by us
        """
        cell_to_update = self.grid[coordinate[0]][coordinate[1]]
        # Anonymization
        for s in ['us', 'them', 'humans']:
            try:
                self.creatures_list[s].pop((coordinate[0], coordinate[1]))
                break
            except KeyError:
                pass
        if number:
            if species == 'humans':
                species_anonymous = 'humans'
            elif species == our_name:
                species_anonymous = 'us'
            else:
                species_anonymous = 'them'
            self.creatures_list[species_anonymous][(coordinate[0], coordinate[1])] = number
        else:
            species_anonymous = None
        cell_to_update.update(species_anonymous, number)

    def update_cell2(self, cell: Cell):
        """Method to update a given cell.

                Arguments:
                    the new cell
                """
        self.grid[cell.x][cell.y].update(cell.creature, cell.number)

        for s in ['us', 'them', 'humans']:
            try:
                self.creatures_list[s].pop((cell.x, cell.y))
                break
            except KeyError:
                pass
        if cell.number:
            self.creatures_list[cell.creature][(cell.x, cell.y)] = cell.number

    def get_cell(self, coordinate=None, x=None, y=None) -> Cell:
        """This method returns a cell element for a given coordinate"""
        if not (coordinate is None):
            return self.grid[coordinate[0]][coordinate[1]]
        if not (x is None or y is None):
            return self.grid[x][y]
        raise RuntimeError("please specify coordinate or x and y")

    def __str__(self):
        grid_s = ""
        for y in range(self.max_y):
            for x in range(self.max_x):
                c = self.grid[x][y].creature if not(self.grid[x][y].creature is None) else "-"
                grid_s += f"{c[0]}-{self.grid[x][y].number}\t"
            grid_s += "\n"
        return grid_s

    def deepcopy(self) -> Board:
        new_board = Board(self.max_x, self.max_y)
        for x in range(self.max_x):
            for y in range(self.max_y):
                if self.grid[x][y].number:
                    new_board.update_cell2(self.grid[x][y])
        return new_board

    def count_creatures(self) -> int:
        return sum(self.creatures_list['us'].values()), sum(self.creatures_list['them'].values()), sum(
            self.creatures_list['humans'].values())
