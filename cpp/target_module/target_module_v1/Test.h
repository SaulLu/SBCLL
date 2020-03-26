#ifndef TEST_H_INCLUDED 
#define TEST_H_INCLUDED 

#include <map>
#include <vector>
#include <array>

#include "Attacker.h"
#include "Target.h"
#include "Attributor.h"
#include "enums.h"

class Test
{
public:
	static std::vector<Attributions> testViableTargets();
	static std::vector<Attributions> testViableTargets2();
	static std::vector<Attributions> testViableTargets3();
};

#endif
