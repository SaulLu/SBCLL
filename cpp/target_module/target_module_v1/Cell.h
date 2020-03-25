#ifndef CELL_H_INCLUDED 
#define CELL_H_INCLUDED 

#include <array>
#include <vector>

#include "enums.h"

class Cell
{
public:
	Cell(const int x, const int y, const Creature creature, const int number);
	
	Creature getCreature();
	int getNumber();

	void update(const Creature creature, const int number);

private:
	static int m_x;
	static int m_y;
	Creature m_creature;
	int m_number;
};

#endif

