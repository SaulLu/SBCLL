import math 
import models.target_engine as target_engine
import models.engine as engine

class Node:
    """Class modelizing a node in the alpha beta tree
    """

    def __init__(self, moves):
        self.moves = moves
        self.potential_boards = engine.get_possible_boards_from_turn(moves)

    def get_score_node(self, heuristic):
        score = 0
        for board, proba in self.potential_boards:
            score += heuristic(board)*proba
        return score

def alphabeta_gen(current_board, player, get_next_moves, current_depth, max_depth, heuristic, alpha, beta):
    
    # on est sur une feuille
    if current_depth == max_depth:
        return (None, heuristic(current_board))
        
    # sinon
    else:
        list_moves = get_next_moves(current_board) # get-next_moves dépend de la strat
        nodes = [Node(moves) for moves in list_moves] # on génère les boards à partir des moves considérés par la strat
        
        if player == "us":
            bestMove = None
            bestScore = -math.inf

            for node in nodes:
                score = 0
                for potential_board, proba_board in node.potential_boards:
                    _, score_board = alphabeta_gen(potential_board, "them", get_next_moves, current_depth+1, max_depth, heuristic, alpha, beta)
                    score += proba_board * score_board

                if score > bestScore:
                    bestScore = score
                    bestMove =node.moves

                if bestScore >= beta:
                    return(bestMove, bestScore)

                alpha = max(alpha, score)
            
        elif player == "them":        
            bestMove = None
            bestScore = math.inf

            for node in nodes:
                score = 0
                for potential_board, proba_board in node.potential_boards:
                    _, score_board = alphabeta_gen(potential_board, "us", get_next_moves, current_depth+1, max_depth, heuristic, alpha, beta)
                    score += proba_board * score_board

                if score < bestScore:
                    bestScore = score
                    bestMove = node.moves

                if alpha >= bestScore:
                    return (bestMove, bestScore)
                
                beta = min(beta, score)
                  
        return (bestMove, bestScore)

def alphabeta(root_board, heuristic, get_next_moves, max_depth):
    return alphabeta_gen(root_board, "us", get_next_moves, 0, max_depth, heuristic, alpha = -math.inf, beta = math.inf)   