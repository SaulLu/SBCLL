"""
This file hosts the basic mechanics of the game
"""
import numpy as np
import itertools
import math
from typing import List, Set, Dict, Tuple, Optional

from models.board import Board
from models.cell import Cell
from models.mov import Mov
from models.battle_engine import *


def apply_possible_board_many_moves(board: Board, moves_list, attacker_species, moves_outputs=None):
    """Method that applies a list of moves to a board, with specified outputs or not
    
    Arguments:
        board {Board} -- the board to change
        moves_list {list}  -- list of moves to apply
        attacker_species {string} -- name of the creature doing the moves (attacker)
        moves_outputs {list}  -- list of specific results to apply if provided, otherwise random during battles
    """
    if moves_outputs is None:
        for move in moves_list:
            apply_possible_board_one_move(board, move, attacker_species)
    else:
        for i in range(len(moves_list)):
            apply_possible_board_one_move(board, moves_list[i], attacker_species,
                                          moves_outputs[i]["output_species"], moves_outputs[i]["output_qty"])


def apply_possible_board_one_move(board, move, attacker_species, output_species=None, output_qty=None):
    """Method that applies the result of one move to a board
    If no output is given (species & qty), output is calculated randomly during battles

      Arguments:
        board {Board} -- the board to change
        move {Mov}  -- the move to apply
        attacker_species {string} -- name of the creature doing the moves (attacker)
        output_species {string}  -- if provided, the surviving species of the defender cell of the move
        output_qty {int}  -- if provided, the number of surviving species of the defender cell of the move
    """
    x_init = move.initial_coordinates[0]
    y_init = move.initial_coordinates[1]
    x_dest = move.arrival_coordinates[0]
    y_dest = move.arrival_coordinates[1]

    defender_cell = board.get_cell(x=x_dest, y=y_dest)

    if output_species is None:
        # Get new states by using random in real time if outputs not given (only one output)
        output = cell_outputs_after_move(defender_cell, attacker_species, move.n_creatures)[0]
        output_species, output_qty = output["output_species"], output["output_qty"]

    new_state_defender_cell = Cell(x_dest, y_dest, output_species, output_qty)
    # if output_qty<0:
    #     print("output qty", output_qty)
    #     raise Exception
    if  board.get_cell(x=x_init, y=y_init).number == move.n_creatures :
        attacker_species = None

    new_state_attacker_cell = Cell(x_init, y_init, attacker_species,
                                   board.get_cell(x=x_init, y=y_init).number - move.n_creatures)

    board.update_cell2(new_state_defender_cell)
    board.update_cell2(new_state_attacker_cell)


def create_possible_boards_many_moves(current_board: Board, moves_list, attacker_species, method=None):
    """Method that returns all the possible boards resulting from a list of moves on a board and their probabilities

    Arguments:
    current_board {Board} -- the original board
    moves_list {list}  -- list of moves to apply
    attacker_species {string} -- name of the creature doing the moves (attacker)
    method {string}  -- None, to have only 1 output OR "esperance" to have 2 outputs (attackers win or lose)

    Returns:
        A list of (board, probability_of_board)
    """
    all_boards_and_probas = []

    all_moves_possibilities = []

    # Get all probable outputs for each move
    for move in moves_list:
        defender_cell = current_board.get_cell(move.arrival_coordinates)
        possible_outputs = cell_outputs_after_move(defender_cell, attacker_species, move.n_creatures, method)
        # Add list of outputs for this move
        all_moves_possibilities.append(possible_outputs)

    # Get all combination by taking only one output for each move each time
    all_combinations = itertools.product(*all_moves_possibilities)

    if not(method is None):
        for combination in all_combinations:
            new_board = current_board.deepcopy()
            apply_possible_board_many_moves(new_board, moves_list, attacker_species, combination)
            print("board validity :", check_validity_board(new_board))
            combination_probabilities = [x["output_proba"] for x in combination]
            board_probability = np.prod(combination_probabilities)
            all_boards_and_probas.append((new_board, board_probability))

        return all_boards_and_probas

    else:
        return_board = current_board.deepcopy()
        apply_possible_board_many_moves(return_board, moves_list, attacker_species)
        print("board validity :", check_validity_board(return_board))
        return [(return_board, 1)]

def check_validity_board(board):
    count = 0 
    for x in range(board.max_x):
            for y in range(board.max_y):
                cell = board.get_cell((x,y))
                if cell.number < 0 :
                    print("negative people")
                    print(move)
                    print(board)
                    count += 1
    if count > 0 :
        return False
    return True
    

def create_possible_boards_one_move(current_board, move, attacker_species, method=None):
    """Method that returns all the possible boards resulting from a move on a board and their probabilities
    
    Arguments:
        current_board {Board} -- the original board
        move {Mov}  -- the move to do
        attacker_species {string} -- name of the creature attacking the cell
        method {string}  -- None, to have only 1 output OR "esperance" to have 2 outputs (attackers win or lose)

    Returns:
        A list of (board, probability_of_board)
    """
    all_possibilities = []
    defender_cell = current_board.get_cell(move.arrival_coordinates)
    possible_outputs = cell_outputs_after_move(defender_cell, attacker_species, move.n_creatures, method)
    for output in possible_outputs:
        new_board = current_board.deepcopy()
        apply_possible_board_one_move(new_board, move, attacker_species, output["output_species"], output["output_qty"])
        all_possibilities.append((new_board, output["output_proba"]))
    return all_possibilities


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


def get_attainable_cells(i_coord: int, j_coord: int, creature, board: Board):
    return [adj for adj in adjacent_cells(i_coord, j_coord, board) if
            board.grid[adj[0]][adj[1]].creature != creature]


def get_cell_moves(cell: Cell, board: Board):
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
            targets = get_attainable_cells(cell.x, cell.y, creature_name, board)
            if len(targets):
                for i in range(cell.number):
                    if np.random.rand() > 0.5:  # will move!
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


def get_distance_between_cells(pos_cell1 : tuple, pos_cell2 : tuple):
    x_1, y_1 = pos_cell1
    x_2, y_2 = pos_cell2
    return max(abs(x_1 - x_2),abs(y_1 - y_2))

def travel_distance(coo1: Tuple[int, int], coo2: Tuple[int, int]) -> int:
    return np.max([abs(coo1[0] - coo2[0]), abs(coo1[1] - coo2[1])])

