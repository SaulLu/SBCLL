from models.engine import Engine

def naive_heuristic(board):
    """ A naive heuristic : calculate the difference between the number of us left and the number if them left.
    
    Arguments:
        board {Board} -- the instance of Board to evaluate
    
    Returns:
        int -- difference between the number of us left and the number of them left
    """

    engine = Engine()
    number_of_us, number_of_them, _ = engine.count_creatures(board)
    
    return number_of_us - number_of_them