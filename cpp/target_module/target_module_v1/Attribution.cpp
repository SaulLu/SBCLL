#include "Attribution.h"

Attribution::Attribution()
{
	start = { -1, -1 };
	target = { -1, -1 };
	number = -1;
}

Attribution::Attribution(Attacker& attacker, Target& target, int number)
{
	this->start = attacker.getLocation();
	this->target = target.getLocation();


	this->number = number;
}

Attribution::Attribution(Attacker& attacker, Attacker& merge_attacker, int number)
{
	this->start = attacker.getLocation();
	this->target = merge_attacker.getLocation();


	this->number = number;
}

Attribution::Attribution(std::array<int, 2> start_loc, std::array<int, 2> arrival_loc, int number_sent)
{
	start = start_loc;
	target = arrival_loc;
	number = number_sent;
}
