"""
This file hosts the functions special to the battles' logic
"""

import numpy as np
import itertools
import math

from models.board import Board
from models.cell import Cell
from models.mov import Mov
import models.engine


def cell_outputs_after_move(defender_cell, attacker_species, attacker_qty, method=None):
    """Method that gives the hypothetic output state of cell if it is under attack .

    Arguments:
        defender_cell {Cell} -- cell that is being attacked
        attacker_species {string} -- name of the creature attacking the cell
        attacker_qty {int}  -- number of attackers

    Returns:
           A list of possible outputs with 3 elements : output_proba, output_species, output_qty
    """    
    outputs = []
    
    # If we join others members of species
    if attacker_species == defender_cell.creature :
        outputs.append({"output_proba":1, "output_species": attacker_species, "output_qty": defender_cell.number + attacker_qty})

    # if we move to an empty cell
    elif defender_cell.creature is None :
        outputs.append({"output_proba":1, "output_species": attacker_species, "output_qty": attacker_qty})
    
    # if we attack humans
    elif defender_cell.creature == "humans":
        if attacker_qty >= defender_cell.number:
            outputs.append({"output_proba":1, "output_species": attacker_species, "output_qty": defender_cell.number + attacker_qty})
        else:
            if method == "esperance":
                outputs = _all_outputs_random_battle(defender_cell, attacker_species, attacker_qty)
            else:
                outputs.append(__random_battle(defender_cell, attacker_species, attacker_qty))
                
    # if we attack our opponents largely (no battles)
    elif attacker_qty >= 1.5 * defender_cell.number:
            outputs.append({"output_proba":1,"output_species": attacker_species, "output_qty": attacker_qty})
    
    # if we attack our opponents with battles
    else:
        if method == "esperance":
            outputs = _all_outputs_random_battle(defender_cell, attacker_species, attacker_qty)
        else:
            # we use real random to generate an output
            outputs.append(__random_battle(defender_cell, attacker_species, attacker_qty))    
    
    return outputs


def _get_proba_to_win(attacker_qty, defender_qty):
    if attacker_qty == defender_qty:
        p = 0.5
    elif attacker_qty < defender_qty:
        p = attacker_qty / (2 * defender_qty)
    else:
        p = -0.5 + attacker_qty / defender_qty
    return p 

    
def _all_outputs_random_battle(defender_cell, attacker_species, attacker_qty):
    
    # 1. Calculate probability p that attackers win
    p = _get_proba_to_win(attacker_qty, defender_cell.number)
    
    # 2. Get mean output of attackers survivors if attackers win
    esperance_attackers_knowing_win = attacker_qty *p

    # add mean nb of humans survivors if they are the defenders
    if defender_cell.creature == "humans":
        esperance_humans = defender_cell.number*p
        esperance_attackers_knowing_win += esperance_humans
    
    esperance_attackers = p * esperance_attackers_knowing_win

    # 3. Get mean output of defenders survivors if attackers lose
    esperance_defenders = defender_cell.number *(1-p) * (1-p)

    return [{"output_proba":p, "output_species": attacker_species, "output_qty":math.ceil(esperance_attackers)},
    {"output_proba":1-p, "output_species": defender_cell.creature, "output_qty":math.ceil(esperance_defenders)}]


def __random_battle(defender_cell, attacker_species, attacker_qty):
    """Private method that simulates a random battle.

    Arguments:
        defender_cell {Cell} -- cell that is being attacked
        attacker_species {string} -- name of the creature attacking the cell
        attacker_qty {int}  -- number of attackers
        
    
    Returns:
        dict{string: <string,int>} -- return the type of the winner species in the cell and their quantity
    """
    # 1. Calculate probability p that attackers win
    p = _get_proba_to_win(attacker_qty, defender_cell.number)

    # 2. Determine winner
    winner_species = np.random.choice([attacker_species, defender_cell.creature], 1, p=[p, 1 - p])[0]

    # 3. Count winner survivors
    if winner_species == attacker_species:
        # Attackers win
        number_winners_survivors = __get_total_survivors(attacker_qty, p)
        if defender_cell.creature == "humans":
            number_humans_survivors = __get_total_survivors(defender_cell.number, p)
            number_winners_survivors += number_humans_survivors
    else:
        # Defenders win
        number_winners_survivors = __get_total_survivors(defender_cell.number, 1 - p)

    return {"output_proba":"No proba", "output_species": winner_species, "output_qty": number_winners_survivors}


def __get_total_survivors(initial_quantity, proba_to_survive):
    """Private method that gets the number of survivors of a given quantity of creatures according to a certain probability to survive.

    Arguments:
        initial_quantity {int} -- initial numbers of creatures
        proba_to_survive {float}  -- probability to survive
    """
    total_survivors = 0
    for _ in range(initial_quantity):
        total_survivors += np.random.choice([1, 0], 1, p=[proba_to_survive, 1 - proba_to_survive])[0]
    return total_survivors
