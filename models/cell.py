class Cell:
    """Class for the content of a cell
    """

    def __init__(self, x, y, creature=None, number=0):
        """Constructor for Cell
                """
        self.number = number
        if self.number == 0:
            self.creature = None  # If there's no one in the cell then creature type is None
        else:
            self.creature = creature
        self.x = x
        self.y = y
        creatures = [None, "humans", "us", "them"]

    def update(self, creature_name, number_creatures):
        """Method to update the cell.
        
        Arguments:
            creature_name {string} -- name of the creature present in this cell
            number_creature {int} -- number of creatures present in this cell
        """

        self.creature = creature_name
        self.number = number_creatures

    def deepcopy(self):
        return Cell(self.x, self.y, self.creature, self.number)

    def __repr__(self):
        return "x: {0}, y: {1}, creature: {2}, qty: {3}".format(self.x, self.y, self.creature, self.number)