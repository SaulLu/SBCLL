import math
import time
import models.target_engine as target_engine
import models.engine as engine

from strategies.alpha_beta import Node, node_pruning, AlphaBeta


class AlphaBetaBreadthFirst(AlphaBeta):
    def __init__(self, t0, timeout, get_next_moves, heuristic, max_depth):
        super().__init__(t0, timeout, get_next_moves, heuristic, max_depth)
        self.tree = [{} for i in range (max_depth)]

    def alphabeta(self, root_board):
        list_moves = self.get_next_moves(root_board, "us") 
        nodes = [Node(moves, root_board, "us", self.heuristic) for moves in
                        list_moves]  # on génère les boards à partir des moves considérés par la strat
        nodes = node_pruning(nodes, self.heuristic, "us")
        self.tree[0][root_board] = nodes, "us"
        self.__generate_tree(nodes, "them", 1) # on génère l'arbre des noeuds, étage par étage jusqu'à ce qu'on ait plus de temps
        return self.__alphabeta_gen(root_board, 0, alpha=-math.inf, beta=math.inf) # on applique alpa_beta

    
    def __generate_tree(self, nodes, player, current_depth):
        if current_depth == self.max_depth: # on est en bas de l'abre
            return

        if time.time() - self.t0 > self.timeout-1: # running out of time 
            print("timeout")
            return

        else:
            next_nodes = []
            for node in nodes:
                for potential_board, _ in node.potential_boards:
                    n_us, n_them, _ = potential_board.count_creatures()
                    if n_us*n_them != 0:
                        list_moves = self.get_next_moves(potential_board, player) 
                        sons = [Node(moves, potential_board, player, self.heuristic) for moves in
                            list_moves]  # on génère les boards à partir des moves considérés par la strat
                        sons = node_pruning(sons, self.heuristic, player)
                        self.tree[current_depth][potential_board] = sons, player
                        next_nodes = next_nodes + sons
            other_player = "us" if player == "them" else "them"
            self.__generate_tree(next_nodes, other_player, current_depth + 1)
    
    def __alphabeta_gen(self, current_board, current_depth, alpha, beta):
        if not(current_board in self.tree[current_depth]): # on est sur une feuille
            return None, self.heuristic(current_board)

        else:
            nodes, player = self.tree[current_depth][current_board]

            if player == "us":
                best_move = None
                best_score = -math.inf

                for node in nodes:
                    score = 0
                    if (time.time() - self.t0 < self.timeout):
                        for potential_board, proba_board in node.potential_boards:
                            _, score_board = self.__alphabeta_gen(potential_board, current_depth+1, alpha, beta)
                            score += proba_board * score_board
                    
                    else: 
                        print("timeout")
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
                    if (time.time() - self.t0 < self.timeout):
                        for potential_board, proba_board in node.potential_boards:
                            _, score_board = self.__alphabeta_gen(potential_board, current_depth+1, alpha, beta)
                            score += proba_board * score_board
                        
                    else: 
                        print("timeout")
                        score = node.basic_score

                    if score < best_score:
                        best_score = score
                        best_move = node.moves

                    if alpha >= best_score:
                        return best_move, best_score

                    beta = min(beta, score)

            return best_move, best_score


    