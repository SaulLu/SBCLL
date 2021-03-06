#ifndef ATTRIBUTION_H_INCLUDED 
#define ATTRIBUTION_H_INCLUDED

#include <array>

#include "Attacker.h"
#include "Target.h"

class Attribution
{
public:
	Attribution();
	Attribution(Attacker& attacker, Target& target, int number);
	Attribution(Attacker& attacker, Attacker& merge_attacker, int number);
	Attribution(std::array<int, 2> start_loc, std::array<int, 2> arrival_loc, int number_sent);
	std::array<int, 2> start;
	std::array<int, 2> target;
	int number;
};

typedef std::pair<std::vector<Attribution>, std::vector<Attribution>> Attributions;

#endif
