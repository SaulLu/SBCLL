#ifndef ATTRIBUTOR_H_INCLUDED 
#define ATTRIBUTOR_H_INCLUDED 

#include <array>
#include <vector>
#include <map>

#include "enums.h"
#include "Move.h"

class Attributor
{
public:
	Attributor(const std::vector<std::array<int, 4>>, const Creature player);
	std::vector<Move> getFeasibleTurns();

private:
	Creature m_player;
	std::map<Creature, std::array<int, 3>> m_creatures;


};


#endif

