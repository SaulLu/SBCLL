import sys
import trace
import threading
import queue
import time
import ctypes


class GetNextMoveCaller(threading.Thread):
    def __init__(self, get_next_moves, board, player, allowed_time, max_x, max_y):
        threading.Thread.__init__(self)
        self.get_next_moves = get_next_moves
        self.board = board
        self.player = player
        self.next_moves = queue.Queue()
        self.allowed_time = allowed_time
        self.finished = False
        self.max_x = max_x
        self.max_y = max_y

    def run(self):
        self.next_moves.put(self.get_next_moves(self.board, self.player, self.allowed_time, self.max_x, self.max_y))
        self.finished = True

    def get_id(self):

        # returns id of the respective thread
        if hasattr(self, '_thread_id'):
            return self._thread_id
        for id, thread in threading._active.items():
            if thread is self:
                return id

    def kill(self):
        thread_id = self.get_id()
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id,
                                                         ctypes.py_object(SystemExit))
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
            print('Exception raise failure')