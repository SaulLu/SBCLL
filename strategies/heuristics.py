#from models.targetEngine import get_feasible_targets

def naive_heuristic(board):
    """ A naive heuristic : calculate the difference between the number of us left and the number if them left.
    
    Arguments:
        board {Board} -- the instance of Board to evaluate
    
    Returns:
        int -- difference between the number of us left and the number of them left
    """
    number_of_us, number_of_them, _ = board.count_creatures()
    
    return number_of_us - number_of_them

def distance_target_difference_heuristic(board):
    feasible_targets_us = get_feasible_targets(board, "us")
    feasible_targets_them = get_feasible_targets(board, "them")

    score_us = __get_score_distance_target(board, feasible_targets_us) 
    score_them = __get_score_distance_target(board, feasible_targets_them) 

    return score_us - score_them

def distance_target_heuristic(board):
    feasible_targets_us = get_feasible_targets(board, "us")
    return __get_score_distance_target(board, feasible_targets_us) 

def __get_score_distance_target(board, dict_feasible_targets):
    score = 0
    for pos,list_targets in dict_feasible_targets:
        for pos_target in list_targets:
            score += board.grid[pos_target].number / (get_distance_between_cells(pos, pos_target)**2) 
    return score

def get_distance_between_cells(pos_cell1, pos_cell2):
    x_1, y_1 = pos_cell1
    x_2, y_2 = pos_cell2
    return max(abs(x_1 - x_2),abs(y_1 - y_2))