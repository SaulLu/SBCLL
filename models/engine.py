class Engine():
    def adjacent_cells(self, i_coord, j_coord, board):
        """Method that returns the index of the existing adjacent cells for a given cell.
        
        Arguments:
            i_coord {int} -- index of row
            j_coord {int} -- index of column
        """
        assert(i_coord>=0 and i_coord<board.max_x,"Row index out of grid")
        assert(((j_coord>=0) and (j_coord<board.max_y)),"Column index out of grid")

        adjacent = []
        for x,y in [(i_coord+i,j_coord+j) for i in (-1,0,1) for j in (-1,0,1) if i != 0 or j != 0]:
            if ((x>=0) and (x<board.max_x) and (y>=0) and (y<board.max_y)):
                adjacent.append((x,y))
        
        return adjacent    
        
    def count_creatures(self, board):
        """Method to count the number of each creature (us, them, humans). 
        
        Arguments:        
            board {Board} -- an instance of Board class to evaluate
        
        Returns:
            (int, int, int) -- the number of each creature in that order :(us, them, humans)
        """
        
        number_of_us = 0
        number_of_them = 0
        number_of_humans = 0

        for i in range(board.max_x):
            for j in range(board.max_y):
                if board[i][j].creature == "us":
                    number_of_us += 1
                elif board[i][j].creature == "them":
                    number_of_them += 1
                elif board[i][j].creature == "humans":
                    number_of_humans += 1
        
        return number_of_us, number_of_them, number_of_humans