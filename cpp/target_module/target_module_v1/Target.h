#ifndef TARGET_H_INCLUDED 
#define TARGET_H_INCLUDED

#include <array>
#include <vector>
#include <map>

#include "enums.h"
#include <algorithm>

class Attacker;
class Target
{
public:
	Target();
	Target(const std::array<int, 2> location, const Creature creature, const int number, const int id);
	int getTakeOver();
	void addAttacker(const int attacker_id);
	bool removeAttacker(const int attacker_id);
	void purgeAttackers(std::map<int, Target>& targets, std::map<int, Attacker>& attackers);
	void clearAttackers();
	const std::array<int, 2> getLocation();

	const std::vector<int>* getAttackersIdsPointer();

	Target operator=(const Target& t);

	static int getNextId();

private:
	static int s_next_id;
	const int m_id;
	const std::array<int, 2> m_location;
	const Creature m_creature;
	const int m_number;
	const int m_takeover;
	std::vector<int> m_attackers_ids;

	static int computeTakeOver(const Creature creature, const int number);
};

#endif

