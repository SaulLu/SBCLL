#ifndef CHECKS_H_INCLUDED 
#define CHECKS_H_INCLUDED

#include <array>
#include <vector>
#include <map>
#include <algorithm>

#include "enums.h"
#include "Attribution.h"

class Checks
{
public:
	static void countTargetError(std::vector<Attributions> all_attributions, std::map<int, Attacker> attackers, std::map<int, Target> targets);
	static TargetError checkAttributions(Attributions attributions, std::map<int, Attacker> attackers, std::map<int, Target> targets);
};

#endif

