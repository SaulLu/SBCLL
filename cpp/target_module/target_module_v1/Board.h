#ifndef BOARD_H_INCLUDED 
#define BOARD_H_INCLUDED 

#include <array>
#include <vector>

#include "enums.h"
#include "Cell.h"

class Board
{
public:
	Board(std::vector<std::array<int, 4>> units_list);


private:
	std::vector<std::vector<Cell>> m_board;
	static int m_max_x;
	static int m_max_y;
};

#endif