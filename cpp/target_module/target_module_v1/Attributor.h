#ifndef ATTRIBUTOR_H_INCLUDED 
#define ATTRIBUTOR_H_INCLUDED 

#include <array>
#include <vector>
#include <map>
#include <chrono>
#include <math.h>

#include "enums.h"
#include "Move.h"
#include "Target.h"
#include "Attacker.h"
#include "Attribution.h"
#include "Checks.h"
#include "Geometry.h"

class Attributor
{
public:
	Attributor(const std::map<Creature, std::vector<std::array<int, 3>>> creatures, const Creature player, const int max_x, const int max_y,
		const double overlap_angle = 22.5, const double timeout = 3600); 
	std::vector<Attributions> getTargetAttribution();

	

private:
	Creature m_player;
	std::map<Creature, std::vector<std::array<int, 3>>> m_creatures;
	std::map<int, Attacker> m_attackers;
	std::map<int, Target> m_targets;
	const double m_timeout;  //in seconds
	std::chrono::system_clock::time_point m_t0;
	const double m_overlap_angle;
	const int m_max_x;
	const int m_max_y;

	void constructTA();
	void setAllTargets();
	void setScopeTargets();
	std::vector<Attributions> recursiveTargetAttribution(Attributions current_attributions, std::map<int, Attacker> attackers,
														std::map<int, Target> targets);
	std::vector<Attributions> applyAttribution(Attributions current_attributions, std::map<int, Attacker> attackers,
												std::map<int, Target> targets, const int target_id, const int attacker_id,
												const int number, bool& infer);
	const int getNextTargetId(std::map<int, Target> targets);
	const int getClosestAlly(const int attacker_id);
	void applyMergeAttribution(Attributions& current_attributions, std::map<int, Attacker>& attackers);
	void applySuicidalAttribution(Attributions& current_attributions, std::map<int, Attacker>& attackers, std::map<int, Target>& targets);
	const double getRemainingTime();
	const bool isRunSituation();
	const std::vector<std::array<int, 2>> getAvailableRunLocations();
	const std::vector<Attributions> applyRunAttribution();
};


#endif

