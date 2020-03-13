"""
This file hosts the basic mechanics of the game
"""
import numpy as np
import itertools
import math

from models.board import Board
from models.cell import Cell
from models.mov import Mov


def apply_possible_board_many_moves(board: Board, moves_list, attacker_species, method=None):
    """Method that apply moves to a board"""
    for move in moves_list:
        apply_possible_board_one_move(board, move, attacker_species, method=None)


def apply_possible_board_one_move(board: Board, move: Mov, attacker_species, method):
    """Method that apply one move to a board"""
    x_init = move.initial_coordinates[0]
    y_init = move.initial_coordinates[1]
    x_dest = move.arrival_coordinates[0]
    y_dest = move.arrival_coordinates[1]

    defender_cell = board.get_cell(x_dest, y_dest)

    new_state_defender_cell = cell_output_if_attacked(defender_cell, attacker_species, move.n_creatures,
                                                      method)
    new_state_attacker_cell = Cell(x_init, y_init, attacker_species,
                                   board.get_cell(x_init, y_init).number - move.n_creatures)

    board.update_cell2(new_state_defender_cell)
    board.update_cell2(new_state_attacker_cell)


def create_possible_board_many_moves(current_board: Board, moves_list, attacker_species, method=None):
    """Method that generates a possible board for any given legal combination of moves"""
    return_board = current_board.deepcopy()
    apply_possible_board_many_moves(return_board, moves_list, attacker_species, method)
    return return_board


def create_possible_board_one_move(current_board: Board, move: Mov, attacker_species, method):
    """Method that generates a possible board for any given legal move"""
    x_init = move.initial_coordinates[0]
    y_init = move.initial_coordinates[1]
    x_dest = move.arrival_coordinates[0]
    y_dest = move.arrival_coordinates[1]

    new_possible_board = current_board.deepcopy()
    defender_cell = new_possible_board.get_cell(x_dest, y_dest)

    new_state_defender_cell = cell_output_if_attacked(defender_cell, attacker_species, move.n_creatures,
                                                      method)
    new_state_attacker_cell = Cell(x_init, y_init, attacker_species,
                                   current_board.get_cell(x_init, y_init).number - move.n_creatures)

    new_possible_board.update_cell2(new_state_defender_cell)
    new_possible_board.update_cell2(new_state_attacker_cell)

    return new_possible_board


def cell_output_if_attacked(defender_cell, attacker_species, attacker_qty, method):
    """Method that gives the hypothetic output state of cell if it is under attack .

    Arguments:
        defender_cell {Cell} -- cell that is being attacked
        attacker_species {string} -- name of the creature attacking the cell
        attacker_qty {int}  -- number of attackers

    :returns
       The new state of the cell
    """
    if defender_cell.creature == "humans":
        if attacker_qty >= defender_cell.number:
            output = {"creature": attacker_species, "number": defender_cell.number + attacker_qty}
        else:
            output = __random_battle(defender_cell, attacker_species, attacker_qty)
    elif attacker_qty >= 1.5 * defender_cell.number:
            assert(attacker_species==defender_cell.creature, "This is not an attack")
        output = {"creature": attacker_species, "number": attacker_qty}
    else:
        output = __random_battle(defender_cell, attacker_species, attacker_qty)
    cell = Cell(defender_cell.x, defender_cell.y, output["creature"], output["number"])
    return cell


def __random_battle(defender_cell, attacker_species, attacker_qty):
    """Private method that simulates a random battle.

        Arguments:
            defender_cell {Cell} -- cell that is being attacked
            attacker_species {string} -- name of the creature attacking the cell
            attacker_qty {int}  -- number of attackers
            
            Returns:
                dict{string: <string,int>} -- return the type of the winner species in the cell and their quantity
            """  
    # 1. Calculate probability p
    if attacker_qty == defender_cell.number:
        p = 0.5
    elif attacker_qty < defender_cell.number:
        p = attacker_qty / (2 * defender_cell.number)
    else:
        p = -0.5 + attacker_qty / defender_cell.number

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

    return {"creature": winner_species, "number": number_winners_survivors}


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


def adjacent_cells(i_coord, j_coord, board):
    """Method that returns the index of the existing adjacent cells for a given cell.

    Arguments:
        i_coord {int} -- index of row
        j_coord {int} -- index of column
    """

    adjacents = []
    for x, y in [(i_coord + i, j_coord + j) for i in (-1, 0, 1) for j in (-1, 0, 1) if i != 0 or j != 0]:
        if (x >= 0) and (x < board.max_x) and (y >= 0) and (y < board.max_y):
            adjacents.append((x, y))

    return adjacents


def get_targetable_cells(i_coord, j_coord, creature, board: Board):
    return [adj for adj in adjacent_cells(i_coord, j_coord, board) if
            board.grid[adj[0]][adj[1]].creature != creature]


def get_cell_moves(cell, board: Board):
    """Lists all the ways to divide (or not) the current group and move the members to adjacent cells.
    Returns all possibilities, including not doing anything.

    Arguments:
        cell {Cell} -- the instance of Cell from which we want to know possible moves
        board {Board} -- the instance of Board

    Returns:
        [array] -- an array containing arrays of the combination of possible Mov instances
    """
    possible_moves = []

    # current cell and adjacent cells
    possible_cells = [(cell.x, cell.y)]
    for adj_cell in adjacent_cells(cell.x, cell.y, board):
        possible_cells.append(adj_cell)

    # all combinations of the integers from 0 to the number of creatures included,
    # contains all possible ways of diving the members present on the cell in different groups
    all_div = itertools.combinations_with_replacement(range(cell.number + 1), len(possible_cells))

    for div in all_div:
        if sum(div) == cell.number:  # possible division, with the correct number of creatures
            permutations = itertools.permutations(div)
            permutations = set(permutations)  # removes duplicates
            for perm in permutations:
                move = []
                for i in range(len(perm)):
                    if perm[i] > 0:
                        if (cell.x, cell.y) != possible_cells[i]:
                            mov = Mov((cell.x, cell.y), perm[i], possible_cells[i])
                            move.append(mov)  # initial coordinates are that of the considered cell
                if len(move) > 0:
                    possible_moves.append(move)

    return possible_moves


def get_possible_turns(board: Board, creature_name):
    """Computes all possible moves for a given board and given creature

    Arguments:
        board {Board} -- the instance of Board to consider
        creature_name {string} -- the creature to be considered, "us" or "them"

    Returns:
        [array] -- an array containing array of Mov instances : each array represents a board
            obtainable from considered board after movs have been played
    """
    moves = []
    # find all cells with correct creatures
    cells = []
    for row in board.grid:
        for cell in row:
            if cell.creature == creature_name:
                cells.append(cell)

    # list all possible moves for each of the cells
    for cell in cells:
        moves_cell = []
        for m in get_cell_moves(cell, board):
            moves_cell.append(m)
        moves.append(moves_cell)

        # combine all different moves for each cell together
    combinations = itertools.product(*moves)

    # identify the move where nothing changes and take it out
    result = []
    for c in combinations:
        flatten_c = []
        for item in c:
            if isinstance(item, list):
                for item_bis in item:
                    flatten_c.append(item_bis)
            else:
                flatten_c.append(item)

        departures = set(x.initial_coordinates for x in flatten_c)
        arrivals = set(x.arrival_coordinates for x in flatten_c)
        if len(list(departures & arrivals)) == 0:
            result.append(flatten_c)

    return result


def get_random_turn(board, creature_name):
    """randomly select a turn for a given board and given creature

    Arguments:
        board {Board} -- the instance of Board to consider
        creature_name {string} -- the creature to be considered, "us" or "them"

    Returns:
        [Mov()] -- an array of Mov instances : it represents a board
            obtainable from considered board after movs have been played
    """
    cells = []
    for row in board.grid:
        for cell in row:
            if cell.creature == creature_name:
                cells.append(cell)

    moves = []
    while len(moves) == 0:
        for cell in cells:
            targets = get_targetable_cells(cell.x, cell.y, creature_name, board)
            if len(targets):
                for i in range(cell.number):
                    if np.random.random() > 0.5:  # will move!
                        target_i = np.random.randint(0, len(targets))
                        moves.append(Mov((cell.x, cell.y), 1, targets[target_i]))
    return moves


def count_creatures(board: Board):
    """Method to count the number of each creature (us, them, humans).

    Arguments:
        board {Board} -- an instance of Board class to evaluate

    Returns:
        (int, int, int) -- the number of each creature in that order :(us, them, humans)
    """

    number_of_us = 0
    number_of_them = 0
    number_of_humans = 0

    for i in range(board.max_x):
        for j in range(board.max_y):
            if board.grid[i][j].creature == "us":
                number_of_us += board.grid[i][j].number
            elif board.grid[i][j].creature == "them":
                number_of_them += board.grid[i][j].number
            elif board.grid[i][j].creature == "humans":
                number_of_humans += board.grid[i][j].number

    return number_of_us, number_of_them, number_of_humans


def reverse_creature(creature):
    if creature == 'us':
        return 'them'
    elif creature == 'them':
        return 'us'
    raise RuntimeError(f"invalid creature name: {creature}")



