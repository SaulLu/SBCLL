import math
import time
import threading
import queue

import models.target_engine as target_engine
import models.engine as engine


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


class GetNextMoveCaller(threading.Thread):
    def __init__(self, get_next_moves, board, player, allowed_time):
        threading.Thread.__init__(self)
        self.get_next_moves = get_next_moves
        self.board = board
        self.player = player
        self.next_moves = queue.Queue()
        self.allowed_time = allowed_time

    def run(self):
        self.next_moves.put(self.get_next_moves(self.board, self.player, 0.95 * self.allowed_time))


class AlphaBeta:
    def __init__(self, t0, timeout, get_next_moves, heuristic, max_depth):
        self.t0 = t0
        self.timeout = timeout
        self.gen_time_max = timeout
        self.last_timeout = 0.90 * timeout
        self.get_next_moves = get_next_moves
        self.heuristic = heuristic
        self.max_depth = max_depth
        self.visited_board_count = 0
        self.generated_nodes_count = 0
        self.generated_boards_count = 0
        self.cut_board_count = 0
        self.depth_reached = 0
        self.timed_out = False
        self.time_per_node = None
        self.random_move = None

    def alphabeta(self, root_board):
        self.timed_out = False
        solution = self.__alphabeta_gen(root_board, "us", 0, alpha=-math.inf, beta=math.inf)
        print(f"\tdepth reached / max: {self.depth_reached} / {self.max_depth}, Timed-out: {self.timed_out}"
              f"\n\tvisited / cut / unvisited / generated boards: {self.visited_board_count} / "
              f"{self.cut_board_count} / "
              f"{self.generated_boards_count + 1 - self.visited_board_count - self.cut_board_count} / "
              f"{self.generated_boards_count}")
        
        return solution

    def get_free_time(self):
        remaining_time = self.last_timeout - (time.time() - self.t0)
        unvisited_boards = self.generated_boards_count + 1 - self.visited_board_count - self.cut_board_count
        reserved_time = unvisited_boards * self.time_per_node
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
            print(f"### A: no time to explore child nodes continue with score: {round(score,0)}")
            return None, score
        else:
            allowed_time = max(0, self.get_free_time() - 0.05 * self.timeout)
            get_next_move_caller = GetNextMoveCaller(self.get_next_moves, current_board, player, allowed_time)
            get_next_move_caller.start()
            try:
                list_moves = get_next_move_caller.next_moves.get(timeout=allowed_time)
            except queue.Empty:
                self.timed_out = True
                score = self.heuristic(current_board)
                print(f"### A: get_next_moves took too long, continue with score: {round(score,0)} remaining free time : {self.get_free_time()}")
                return None, score

            nodes = []
            for moves in list_moves:
                if not self.random_move and current_depth==0:
                    self.random_move = moves

                if self.get_free_time() <= 0.2:
                    self.timed_out = True
                    score = self.heuristic(current_board)
                    if player == "us":
                        print(f"### A: ('us') Break nodes generation with score: {round(score,0)}")
                    else:
                        print(f"### A: ('them') Break nodes generation with score: {round(score,0)}")
                    return None, score
                nodes.append(Node(moves, current_board, player, self.heuristic))

            nodes = node_pruning(nodes, self.heuristic, player)
            self.generated_nodes_count += len(nodes)
            self.generated_boards_count += sum(map(lambda x: len(x.potential_boards), nodes))

            if player == "us":
                best_move = None
                best_score = -math.inf

                for i_node, node in enumerate(nodes):
                    score = 0

                    if self.get_free_time() > self.time_per_node * len(node.potential_boards):
                        for potential_board, proba_board in node.potential_boards:
                            _, score_board = self.__alphabeta_gen(potential_board, "them", current_depth + 1, alpha,
                                                                  beta)
                            score += proba_board * score_board
                    else:
                        print(f"### A: ('us') Timeout max limit reached: {time.time() - self.t0}, remaining free time : {self.get_free_time()}, with current best_score: {round(best_score,0)} at the {current_depth} depth")
                        self.timed_out = True
                        if best_score == -math.inf:
                            best_score = node.basic_score
                        return best_move, best_score

                    if score > best_score and node.moves:
                        best_score = score
                        best_move = node.moves
                        if current_depth == 0:
                            print(f"### O: ('us') At the root found a best_move with a score of {round(best_score,0)}")

                    if best_score >= beta:
                        self.cut_board_count += sum(map(lambda x: len(x.potential_boards), nodes[i_node + 1:]))
                        # print(f"### O: ('us') At the {current_depth} depth cut exploration and return a best_move with a score of {round(best_score,0)}")
                        return best_move, best_score

                    alpha = max(alpha, score)
                
                # print(f"### A: ('us') Exploration of the {current_depth} depth finished, return a best_move with {round(best_score,0)}")


            elif player == "them":
                best_move = None
                best_score = math.inf

                for i_node, node in enumerate(nodes):
                    score = node.basic_score
                    if self.get_free_time() > 0:
                        for potential_board, proba_board in node.potential_boards:
                            _, score_board = self.__alphabeta_gen(potential_board, "us", current_depth + 1, alpha, beta)
                            score += proba_board * score_board
                    else:
                        print(f"### A: ('them') Timeout max limit reached: {time.time() - self.t0}, remaining free time : {self.get_free_time()}, current best_score: {round(best_score,0)} at the {current_depth} depth")
                        self.timed_out = True
                        if best_score == math.inf:
                            best_score = node.basic_score
                        return best_move, best_score

                    if score < best_score and node.moves:
                        best_score = score
                        best_move = node.moves
                        if current_depth == 0:
                            print(f"### O: ('them') At the root found a best_move with a score of {round(best_score,0)}")

                    if alpha >= best_score:
                        self.cut_board_count += sum(map(lambda x: len(x.potential_boards), nodes[i_node + 1:]))
                        # print(f"### O: ('them') At the {current_depth} depth cut exploration and return a best_move with a score of {round(best_score,0)}")
                        return best_move, best_score

                    beta = min(beta, score)
                
                # print(f"### A: ('them') Exploration of the {current_depth} depth finished, return a best_move with {round(best_score,0)}")

            if current_depth == 0 and not best_move:
                best_move = self.random_move
                print(f"best move replace with: {best_move}")

            return best_move, best_score

    def __get_time_per_node(self, current_board):
        t0 = time.time()
        _ = self.heuristic(current_board)
        return time.time() - t0

    # def add_infos(self, turn_time=None, 
    #                 depth_reached=None,
    #                 depth_max=None,
    #                 Timed_out=None,
    #                 visited=None,
    #                 cut=None,
    #                 unvisited=None, 
    #                 generated_boards=None,
    #                 random_move=None):
        
    #     path_metrics = os.path.join('test_maps',"metrics.csv")
    #     with open(path_metrics, "r") as f:
    #         reader = csv.reader(f)
    #         mylist = list(reader)
    #         f.close()

    #     mylist[-1][3] = turn_time
    #     # mylist[-1][4] = depth_reached
    #     # mylist[-1][5] = depth_max
    #     # mylist[-1][6] = Timed_out
    #     # mylist[-1][7] = visited
    #     # mylist[-1][8] = cut
    #     # mylist[-1][9] = unvisited
    #     # mylist[-1][10] = generated_boards

    #     with open(path_metrics, 'w', newline = '') as f:
    #         csv_writer = csv.writer(f)
            # csv_writer.writerows(mylist)