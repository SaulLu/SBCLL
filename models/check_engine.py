from models.mov import Mov
from models.board import Board

def check_mov_validity(board : Board, mov : Mov):
    if (mov.initial_coordinates[0]<0 or mov.initial_coordinates[1] < 0):
        print("Initial coordinates out of bounds")
        return (False)
    if (mov.initial_coordinates[0]>board.max_x or mov.initial_coordinates[1] > board.max_y):
        print("Initial coordinates out of bounds")
        return (False)
    if (mov.arrival_coordinates[0]<0 or mov.arrival_coordinates[1] < 0):
        print("Arrival coordinates out of bounds")
        return (False)
    if (mov.arrival_coordinates[0]>board.max_x or mov.arrival_coordinates[1] > board.max_y):
        print("Arrival coordinates out of bounds")
        return (False)
    if (mov.n_creatures < 0):
        print("Negative number of creatures to move")
        return (False)
    if (mov.n_creatures > board.grid[mov.initial_coordinates].number):
        print("Too many creatures to move")
        return (False)
    if  mov is None: 
        print("This move is None")
        return (False)

    return True

def check_moves_validity(board : Board, moves : list):
    if moves is None:
        print("This list of moves is None")
        return False

    creatures_leaving = {}
    for mov in moves: 
        if not(mov.initial_coordinates in creatures_leaving):                
            creatures_leaving[mov.initial_coordinates] = mov.n_creatures
        else:
            creatures_leaving[mov.initial_coordinates] += mov.n_creatures
        if not(check_mov_validity(board, mov)):
            return False
        
    for coord in creatures_leaving:
        if board[coord].number < creatures_leaving[coord]:
            print "Trying to move too many creatures"
            return False
            
    return True

def check_board_validity(move):
    pass