class Mov:
    """
    This class describe the movement from a number of creatures of the same initial Cell
    """
    def __init__(self, init, n_creatures, arrival_coordinates):
        self.arrival_coordinates = arrival_coordinates
        self.initial_coordinates = init
        self.n_creatures = n_creatures

    def __repr__(self):
        return f"Mov() :initial_coordinates : {self.initial_coordinates}, n_creatures : {self.n_creatures}," \
               f" arrival_coordinates : {self.arrival_coordinates} "

    def __str__(self):
        return f"initial_coordinates : {self.initial_coordinates}, n_creatures : {self.n_creatures}," \
               f" arrival_coordinates : {self.arrival_coordinates}"
