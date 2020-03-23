import math
import time
import models.target_engine as target_engine
import models.engine as engine


def node_pruning(nodes, heuristic, player):
    """This function makes a pruning of all"""
    L = []
    for node in nodes:
        score = 0
        for board, probability_board in node.potential_boards:
            score += heuristic(board) * probability_board
        L.append((node, score))

    if player == "us":
        L = sorted(L, key=lambda x: x[1])
    else:
        L = sorted(L, key=lambda x: x[1], reverse=True)

    # print("initi", len(L))
    # print("scores", [round(x[1],2) for x in L])

    # [x[0] for x in L[:min(len(L), 5)]]

    # garder seulement le "peloton de tête" si la liste est de taille > 3
    if len(L) > 3:
        L_centered = [(x[0],x[1]+L[-1][1]) for x in L] # recentrer les scores pour que le premier ne soit jamais 0
        # on élimine tous les noeuds dont le score est plus de 50% moins bon que le premier élément (qui est le meilleur)
        output = []
        for item in L_centered:
            if player == "us":
                if item[1] < (L_centered[0][1] + (L_centered[0][1]/2)):
                    output.append(item)
            else:
                if item[1] > (L_centered[0][1] - (L_centered[0][1]/2)):
                    output.append(item)
        # print("kept nodes", [round(x[1],2) for x in output])
        return [x[0] for x in output]
    else:
        return [x[0] for x in L]


class Node:
    """Class modelling a node in the alpha beta tree
    """

    def __init__(self, moves, board, player, heuristic):
        self.moves = moves
        self.potential_boards = engine.create_possible_boards_many_moves(board, moves, player, method="esperance")
        self.basic_score = self.get_score_node(heuristic)

    def get_score_node(self, heuristic):
        score = 0
        for board, proba in self.potential_boards:
            score += heuristic(board) * proba
        return score


class AlphaBeta:
    def __init__(self, t0, timeout, get_next_moves, heuristic, max_depth):
        self.t0 = t0
        self.timeout = timeout
        self.get_next_moves = get_next_moves
        self.heuristic = heuristic
        self.max_depth = max_depth

    def alphabeta(self, root_board):
        return self.__alphabeta_gen(root_board, "us", 0, alpha=-math.inf, beta=math.inf)

    def __alphabeta_gen(self, current_board, player, current_depth, alpha, beta):
        n_us, n_them, _ = current_board.count_creatures()
        if current_depth == self.max_depth or n_us * n_them == 0:  # on est sur une feuille
            return None, self.heuristic(current_board)

        if time.time() - self.t0 > self.timeout:  # running out of time
            print("timeout", current_depth)
            return None, self.heuristic(current_board)

        else:
            list_moves = self.get_next_moves(current_board, player)  # get_next_moves dépend de la strat
            nodes = [Node(moves, current_board, player, self.heuristic) for moves in
                     list_moves]  # on génère les boards à partir des moves considérés par la strat
            nodes = node_pruning(nodes, self.heuristic, player)

            if player == "us":
                best_move = None
                best_score = -math.inf

                for node in nodes:
                    score = 0
                    if time.time() - self.t0 < self.timeout:
                        for potential_board, proba_board in node.potential_boards:
                            _, score_board = self.__alphabeta_gen(potential_board, "them", current_depth + 1, alpha,
                                                                  beta)
                            score += proba_board * score_board

                    else:
                        print("timeout", current_depth)
                        score = node.basic_score

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
                    score = node.basic_score
                    if time.time() - self.t0 < self.timeout:
                        for potential_board, proba_board in node.potential_boards:
                            _, score_board = self.__alphabeta_gen(potential_board, "us", current_depth + 1, alpha, beta)
                            score += proba_board * score_board

                    else:
                        print("timeout", current_depth)
                        score = node.basic_score

                    if score < best_score:
                        best_score = score
                        best_move = node.moves

                    if alpha >= best_score:
                        return best_move, best_score

                    beta = min(beta, score)

            return best_move, best_score
