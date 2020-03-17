def check_move_validity(move):
    pass


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
    