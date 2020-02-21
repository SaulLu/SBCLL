import numpy as np

class Engine:

    def __init__(self):
        pass

    def cell_output_if_attacked(self, defender_cell, attacker_species, attacker_qty):
        """Method that gives the hypothetic output state of the cell if it is under attack .
        
        Arguments:
            attacker_species {string} -- name of the creature attacking the cell
            attacker_qty {int}  -- number of attackers  
        """  
        if defender_cell.creature == "humans":
            if attacker_qty >= defender_cell.number :
                output = {"creature":attacker_species, "number": defender_cell.number + attacker_qty}
            else:
                output = self.__random_battle(attacker_species,attacker_qty,defender_cell) 
        elif attacker_qty >= 1.5*defender_cell.number:
            output = {"creature":attacker_species, "number": attacker_qty}
        else:
            output = self.__random_battle(attacker_species,attacker_qty,defender_cell)
        return output

    def __random_battle(self, attacker_species, attacker_qty, defender_cell):
            """Private method that simulates a random battle.
            
            Arguments:
                attacker_species {string} -- name of the creature attacking the cell
                attacker_qty {int}  -- number of attackers
                defender_species {string} -- name of the creature attacking the cell
                defender_qty {int}  -- number of attackers 
            """ 
            # 1. Calculate probability p
            if attacker_qty == defender_cell.number :
                p = 0.5
            elif attacker_qty < defender_cell.number:
                p = attacker_qty / (2*defender_cell.number)
            else:
                p= -0.5 + attacker_qty/defender_cell.number
            
            # 2. Determine winner
            winner_species = np.random.choice([attacker_species, defender_cell.creature], 1, p=[p, 1-p])[0]
        
            # 3. Count winner survivors
            if winner_species==attacker_species:
                # Attackers win
                number_winners_survivors =  self.__get_total_survivors(attacker_species, p)
                if defender_cell.species == "humans":
                    number_humans_survivors = self.__get_total_survivors(defender_cell.number, p)
                    number_winners_survivors += number_humans_survivors
            else:
                # Defenders win
                number_winners_survivors =  self.__get_total_survivors(defender_cell.number, 1-p)
            
            return {"creature":winner_species, "number": number_winners_survivors}

    def __get_total_survivors(self, initial_quantity, proba_to_survive):
        """Private method that gets the number of survivors of a given quantity of creatures according to a certain probability to survive.
        
        Arguments:
            initial_quantity {int} -- initial numbers of creatures
            proba_to_survive {float}  -- probability to survive
        """ 
        total_survivors = 0
        for i in range(initial_quantity):
            total_survivors += np.random.choice([1, 0], 1, p=[proba_to_survive, 1-proba_to_survive])[0]
        return total_survivors
            
