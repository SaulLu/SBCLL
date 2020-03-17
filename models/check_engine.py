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
    if (mov.n_creatures > board.grid[mov.initial_coordinates]):
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
        
    for mov in moves: 
        if not(check_mov_validity(board, mov)):
            return False
    return True

def check_board_validity(board):
    
    if board is None :
        return False
    
    count = 0 
    bad_cells = []
    for x in range(board.max_x):
            for y in range(board.max_y):
                cell = board.get_cell((x,y))
                if cell.number < 0 :
                    bad_cells.append(cell)
                    count += 1
    if count > 0 :
        print("The board is not valid")
        return False
    
    return True

def check_boards_validity(list_boards: list):
    
    if list_boards is None :
        return False

    for board in list_boards:
        if not(check_board_validity(board)):
            print("The boards are not valid")
            return False

    return True
    