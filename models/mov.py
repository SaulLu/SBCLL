class Mov:
    def __init__(self, init, numb, arriv):
        self.coord_arriv = arriv
        self.coord_init = init
        self.number_indiv = numb

    def __repr__(self):
        return f"Mov() :coord_init : {self.coord_init}, number : {self.number_indiv}, coord_arriv : {self.coord_arriv}"

    def __str__(self):
        return f"coord_init : {self.coord_init}, number : {self.number_indiv}, coord_arriv : {self.coord_arriv}"