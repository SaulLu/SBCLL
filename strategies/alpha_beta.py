import math
import models.target_engine as target_engine
import models.engine as engine


class Node:
    """Class modelizing a node in the alpha beta tree
    """

    def __init__(self, moves, board, player):
        self.moves = moves
        self.potential_boards = engine.create_possible_boards_many_moves(board, moves, player, method="esperance")
        all_boards = [x[0] for x in self.potential_boards]
        all_probas = [x[1] for x in self.potential_boards]

    # def get_score_node(self, heuristic):
    #     score = 0
    #     for board, proba in self.potential_boards:
    #         score += heuristic(board)*proba
    #     return score


def alphabeta_gen(current_board, player, get_next_moves, current_depth, max_depth, heuristic, alpha, beta):
    n_us, n_them, _ = current_board.count_creatures()
    if current_depth == max_depth or n_us * n_them == 0:# on est sur une feuille
        return None, heuristic(current_board)

    # sinon
    else:
        list_moves = get_next_moves(current_board, player)  # get-next_moves dépend de la strat
        nodes = [Node(moves, current_board, player) for moves in
                 list_moves]  # on génère les boards à partir des moves considérés par la strat

        if player == "us":
            best_move = None
            best_score = -math.inf

            for node in nodes:
                score = 0
                for potential_board, proba_board in node.potential_boards:
                    _, score_board = alphabeta_gen(potential_board, "them", get_next_moves, current_depth + 1,
                                                   max_depth, heuristic, alpha, beta)
                    score += proba_board * score_board

                if score > best_score:
                    best_score = score
                    best_move = node.moves

                if best_score >= beta:
                    return best_move, best_score

                alpha = max(alpha, score)

        elif player == "them":
            best_move = None
            best_score = math.inf

            for node in nodes:
                score = 0
                for potential_board, proba_board in node.potential_boards:
                    _, score_board = alphabeta_gen(potential_board, "us", get_next_moves, current_depth + 1, max_depth,
                                                   heuristic, alpha, beta)
                    score += proba_board * score_board

                if score < best_score:
                    best_score = score
                    best_move = node.moves

                if alpha >= best_score:
                    return best_move, best_score

                beta = min(beta, score)

        return best_move, best_score


def alphabeta(root_board, heuristic, get_next_moves, max_depth):
    return alphabeta_gen(root_board, "us", get_next_moves, 0, max_depth, heuristic, alpha=-math.inf, beta=math.inf)
