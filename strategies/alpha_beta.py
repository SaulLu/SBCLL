import math
import time
import models.target_engine as target_engine
import models.engine as engine


def node_pruning(nodes, heuristic, player):
    """This function makes a pruning of all"""
    L = []
    mult = 1 if player == 'us' else -1
    for node in nodes:
        score = 0
        for board, probability_board in node.potential_boards:
            score += heuristic(board) * probability_board
        L.append((node, mult * score))

    L = sorted(L, key=lambda x: x[1], reverse=True)

    # print("initi", len(L))
    # print("scores", [round(x[1],2) for x in L])

    # [x[0] for x in L[:min(len(L), 5)]]

    # garder seulement le "peloton de tête" si la liste est de taille > 3
    len_L = len(L)
    if len_L > 3:
        best_score = L[0][1]
        worst_score = L[-1][1]
        score_range = best_score - worst_score
        if score_range:
            limit_index = 0
            while (L[limit_index][1] - worst_score) / score_range > 0.3 and limit_index < len_L :
                limit_index += 1
            limit_index = min(limit_index, len_L)
            return [x[0] for x in L[0:limit_index]]
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
        self.nodes_count = 0
        self.depth_reached = 0
        self.timed_out = False

    def alphabeta(self, root_board):
        self.timed_out = False
        solution = self.__alphabeta_gen(root_board, "us", 0, alpha=-math.inf, beta=math.inf)
        print(f"I explored : {self.nodes_count} nodes with a max depth of {self.depth_reached}")
        return solution

    def __alphabeta_gen(self, current_board, player, current_depth, alpha, beta):
        self.depth_reached = max(current_depth, self.depth_reached)
        n_us, n_them, _ = current_board.count_creatures()
        if current_depth == self.max_depth or n_us * n_them == 0:  # on est sur une feuille
            return None, self.heuristic(current_board)

        if time.time() - self.t0 > self.timeout:  # running out of time
            self.timed_out = True
            return None, self.heuristic(current_board)

        else:
            list_moves = self.get_next_moves(current_board, player)  # get_next_moves dépend de la strat
            nodes = [Node(moves, current_board, player, self.heuristic) for moves in
                     list_moves]  # on génère les boards à partir des moves considérés par la strat
            nodes = node_pruning(nodes, self.heuristic, player)
            self.nodes_count += len(nodes)

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
                        self.timed_out = True
                        score = node.basic_score

                    if score < best_score:
                        best_score = score
                        best_move = node.moves

                    if alpha >= best_score:
                        return best_move, best_score

                    beta = min(beta, score)

            return best_move, best_score
