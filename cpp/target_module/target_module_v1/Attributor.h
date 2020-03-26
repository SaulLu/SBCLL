#ifndef ATTRIBUTOR_H_INCLUDED 
#define ATTRIBUTOR_H_INCLUDED 

#include <array>
#include <vector>
#include <map>

#include "enums.h"
#include "Move.h"
#include "Target.h"
#include "Attacker.h"
#include "Attribution.h"
#include "Checks.h"

class Attributor
{
public:
	Attributor(const std::map<Creature, std::vector<std::array<int, 3>>> creatures, const Creature player);
	std::vector<Attributions> getTargetAttribution();

	

private:
	Creature m_player;
	std::map<Creature, std::vector<std::array<int, 3>>> m_creatures;
	std::map<int, Attacker> m_attackers;
	std::map<int, Target> m_targets;

	void constructTA();
	std::vector<Attributions> recursiveTargetAttribution(Attributions current_attributions, std::map<int, Attacker> attackers,
														std::map<int, Target> targets);
	std::vector<Attributions> applyAttribution(Attributions current_attributions, std::map<int, Attacker> attackers,
												std::map<int, Target> targets, const int target_id, const int attacker_id,
												const int number, bool& infer);
	const int getNextTargetId(std::map<int, Target> targets);
	const int getClosestAlly(const int attacker_id);
	void applyMergeAttribution(Attributions& current_attributions, std::map<int, Attacker>& attackers);
	void applySuicidalAttribution(Attributions& current_attributions, std::map<int, Attacker>& attackers, std::map<int, Target>& targets);
};


#endif

