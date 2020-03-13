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

def alphabeta_gen(current_board, player, getNextMoves, current_depth, initial_depth, max_depth, heuristic, alpha, beta):
    
    # on est sur une feuille
    if current_depth == 0:
        return (None, heuristic(current_board))
        
    #sinon
    else:
        list_moves = getNextMoves(current_board) #A adpater en ft des strats
        nodes = [Node(moves) for moves in list_moves]
        
        if player == "us":
            bestMove = None
            bestScore = -math.inf

            # if initial_depth == current_depth: #Je ne sais pas à quoi ça sert de les ordonner, surement un moyen d'accèlérer la suite
            #     couplage = [(potential_boards[i], moves[i]) for i in range(len(moves))]
            #     couplage_sorted = sorted(couplage, key = lambda x: sort_game_func(x[0], scoring_function), reverse=True)
                
            #     potential_boards = [x[0] for x in couplage_sorted]
            #     moves = [x[1] for x in couplage_sorted]

            for node in nodes:
                score = 0
                for potential_board, proba_board in node.potential_boards:
                    _, score_board = alphabeta_gen(potential_board, "them", getNextMoves, current_depth-1, initial_depth, max_depth, heuristic, alpha, beta)
                    score += proba_board * score_board

                if current_depth == max_depth:
                    return (bestMove, bestScore)
                
                if score > bestScore:
                    alpha = max(alpha, score)
                    bestScore = score
                    bestMove =node.moves
                        
                if alpha >= beta:
                    return (bestMove, bestScore)
                  
            return (bestMove, bestScore)
            
        elif player == "them":
        
            bestMove = None
            bestScore = math.inf

            for node in nodes:
                score = 0
                for potential_board, proba_board in node.potential_boards:
                    _, score_board = alphabeta_gen(potential_board, "us", getNextMoves, current_depth-1, initial_depth, max_depth, heuristic, alpha, beta)
                    score += proba_board * score_board

                if score < bestScore:
                    beta = min(beta, score)
                    bestScore = score
                    bestMove = node.moves

                if alpha >= beta:
                    return (bestMove, bestScore)
                  
            return (bestMove, bestScore)

def alphabeta(current_board, current_depth, heuristic, getNextMoves, max_depth):
    return alphabeta_gen(current_board, "us", getNextMoves, current_depth, current_depth, max_depth, heuristic, alpha = -10000, beta = 10000)   
  	#Normal d'avoir 2 fois current_depth ici, puisqu'au premier tour current_depth = initial_depth