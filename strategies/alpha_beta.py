import math
import time
import threading
import queue

import models.target_engine as target_engine
import models.engine as engine
from strategies.caller import GetNextMoveCaller


def node_pruning(nodes, heuristic, player):
    """This function makes a pruning of all"""
    L = []
    mult = 1 if player == 'us' else -1
    for node in nodes:
        L.append((node, mult * node.basic_score))

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
            while (L[limit_index][1] - worst_score) / score_range > 0.3 and limit_index < len_L:
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
        self.gen_time_max = timeout
        self.last_timeout = 0.98 * timeout
        self.get_next_moves = get_next_moves
        self.heuristic = heuristic
        self.max_depth = max_depth
        self.visited_board_count = 0
        self.generated_nodes_count = 0
        self.generated_boards_count = 0
        self.generated_moves_count = 0
        self.cut_node_count = 0
        self.depth_reached = 0
        self.timed_out = False
        self.time_per_node = None
        self.random_move = None

    def alphabeta(self, root_board):
        self.timed_out = False
        solution = self.__alphabeta_gen(root_board, "us", 0, alpha=-math.inf, beta=math.inf)
        print(f"\tdepth reached / max: {self.depth_reached} / {self.max_depth}, Timed-out: {self.timed_out}"
              f"\n\tvisited / unvisited / generated boards: {self.visited_board_count} / "
              f"{self.generated_boards_count + 1 - self.visited_board_count} / "
              f"{self.generated_boards_count}\n\tcut nodes: {self.cut_node_count},"
              f" unvisited_moves: {self.generated_moves_count - self.generated_nodes_count - self.cut_node_count}")
        return solution

    def get_free_time(self):
        remaining_time = self.last_timeout - (time.time() - self.t0)
        ungenerated_nodes = self.generated_moves_count - self.generated_nodes_count - self.cut_node_count
        unvisited_board = self.generated_boards_count - self.visited_board_count 
        reserved_time = (ungenerated_nodes + unvisited_board) * self.time_per_node
        return remaining_time - reserved_time

    def __alphabeta_gen(self, current_board, player, current_depth, alpha, beta):
        self.visited_board_count += 1

        if not self.time_per_node:
            self.time_per_node = self.__get_time_per_node(current_board)

        self.depth_reached = max(current_depth, self.depth_reached)
        n_us, n_them, _ = current_board.count_creatures()
        if current_depth == self.max_depth or n_us * n_them == 0:  # on est sur une feuille
            score = self.heuristic(current_board)
            # if player == "us":
            #     print(f"### O: We are on a leaf 'us' with current score {round(score,0)}")
            # else:
            #     print(f"### O: We are on a leaf 'them' with current score {round(score,0)}")
            return None, score

        if self.get_free_time() <= 0:  # no more time to generate nodes
            self.timed_out = True
            score = self.heuristic(current_board)
            # print(f"### A: no time to explore child nodes continue with score: {round(score,0)}")
            return None, score
        else:
            allowed_time = max(0, self.get_free_time() - 0.05 * self.timeout)
            allowed_t0 = time.time()
            get_next_move_caller = GetNextMoveCaller(self.get_next_moves, current_board, player, allowed_time)
            get_next_move_caller.start()
            list_moves = []
            while time.time() - allowed_t0 < allowed_time and len(list_moves) == 0:
                try:
                    list_moves = get_next_move_caller.next_moves.get(timeout=0.001)
                except queue.Empty:
                    pass
            get_next_move_caller.kill()
            len_list_moves = len(list_moves)
            if len_list_moves == 0:  # did not retrieve the possible next moves
                self.timed_out = True
                score = self.heuristic(current_board)
                print(f"### A: get_next_moves took too long (f:{get_next_move_caller.finished}, continue with score:"
                      f" {round(score,0)} remaining free time : {self.get_free_time()}")
                return None, score

            self.generated_moves_count += len_list_moves
            if player == "us":
                best_move = None
                best_score = -math.inf

                for i_moves, moves in enumerate(list_moves):
                    node = Node(moves, current_board, player, self.heuristic)
                    self.generated_boards_count += len(node.potential_boards)
                    self.generated_nodes_count += 1
                    score = 0

                    if self.get_free_time() > 0:
                        for potential_board, proba_board in node.potential_boards:
                            _, score_board = self.__alphabeta_gen(potential_board, "them", current_depth + 1, alpha,
                                                                  beta)
                            score += proba_board * score_board
                    else:
                        # print(f"### A: ('us') Timeout max limit reached: {time.time() - self.t0}, remaining free time :"
                        #       f" {self.get_free_time()}, with current best_score: {round(best_score,0)} at "
                        #       f"the {current_depth} depth")
                        self.timed_out = True
                        if best_score == -math.inf:
                            return node.moves, node.basic_score
                        return best_move, best_score

                    if score > best_score and node.moves and score != math.inf:
                        best_score = score
                        best_move = node.moves
                        # if current_depth == 0:
                        #     print(f"### O: ('us') At the root found a best_move with a score of {round(best_score,0)}")

                    if best_score >= beta:
                        self.cut_node_count += len_list_moves - i_moves - 1
                        return best_move, best_score

                    alpha = max(alpha, score)
                
                # print(f"### A: ('us') Exploration of the {current_depth} depth finished, "
                #       f"return a best_move with {round(best_score,0)}")

            elif player == "them":
                best_move = None
                best_score = math.inf

                for i_moves, moves in enumerate(list_moves):
                    node = Node(moves, current_board, player, self.heuristic)
                    self.generated_boards_count += len(node.potential_boards)
                    self.generated_nodes_count += 1
                    score = 0
                    if self.get_free_time() > 0:
                        for potential_board, proba_board in node.potential_boards:
                            _, score_board = self.__alphabeta_gen(potential_board, "us", current_depth + 1, alpha, beta)
                            score += proba_board * score_board
                    else:
                        # print(f"### A: ('them') Timeout max limit reached: {time.time() - self.t0}, remaining free time"
                        #       f" : {self.get_free_time()}, current best_score: {round(best_score,0)} at "
                        #       f"the {current_depth} depth")
                        self.timed_out = True
                        if best_score == math.inf:
                            return node.moves, node.basic_score
                        return best_move, best_score

                    if score < best_score and node.moves and score != -math.inf:
                        best_score = score
                        best_move = node.moves
                        # if current_depth == 0:
                            # print(f"### O: ('them') At the root found a best_move with a score of {round(best_score,0)}")

                    if alpha >= best_score:
                        self.cut_node_count += len_list_moves - i_moves - 1
                        return best_move, best_score

                    beta = min(beta, score)
                
                # print(f"### A: ('them') Exploration of the {current_depth} depth finished,"
                #       f" return a best_move with {round(best_score,0)}")

            if current_depth == 0 and not best_move:
                best_move = self.random_move
                # print(f"best move replace with: {best_move}")

            return best_move, best_score

    def __get_time_per_node(self, current_board):
        t0 = time.time()
        _ = self.heuristic(current_board)
        return time.time() - t0

    def add_infos(turn_time=None, 
                    depth_reached=None,
                    depth_max=None,
                    Timed_out=None,
                    visited=None,
                    cut=None,
                    unvisited=None, 
                    generated_boards=None,
                    ):
        
        path_metrics = '../' + os.path.join('test_maps',"metrics.csv")
        with open(path_metrics, "r") as f:
            reader = csv.reader(f)
            mylist = list(reader)
            f.close()

        mylist[-1][4] = turn_time
        # mylist[-1][5] = depth_reached
        # mylist[-1][6] = depth_max
        # mylist[-1][7] = Timed_out
        # mylist[-1][8] = visited
        # mylist[-1][9] = cut
        # mylist[-1][10] = unvisited
        # mylist[-1][11] = generated_boards

        with open(path_metrics, 'w', newline = '') as f:
            csv_writer = csv.writer(f)
            csv_writer.writerows(mylist)