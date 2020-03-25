#ifndef TARGET_H_INCLUDED 
#define TARGET_H_INCLUDED

#include <vector>
#include <map>

#include "enums.h"
#include <algorithm>

class Attacker;
class Target
{
public:
	Target(const int x, const int y, const Creature creature, const int number);
	int getMinTakeOver();
	void addAttacker(const int attacker_id);
	void removeAttacker(const int attacker_id);
	static int getNextId();
private:
	static int s_next_id;
	const int m_id;
	const int m_x;
	const int m_y;
	const Creature m_creature;
	const int m_number;
	const int m_min_takeover;
	std::vector<int> m_attackers_ids;

	static int MinTakeOver(const Creature creature, const int number);
};

#endif

