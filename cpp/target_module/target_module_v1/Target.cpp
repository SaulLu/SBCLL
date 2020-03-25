#include "Target.h"
#include "Attacker.h"

using namespace std;

Target::Target(const int x, const int y, const Creature creature, const int number)
		: m_x(x), m_y(y), m_creature(creature), m_number(number), m_min_takeover(MinTakeOver(creature, number)), m_id(getNextId())
{

}

int Target::getMinTakeOver()
{
	return m_min_takeover;
}

void Target::addAttacker(const int attacker_id)
{
	m_attackers_ids.push_back(attacker_id);
}

void Target::removeAttacker(const int attacker_id)
{
	vector<int>::iterator position = find(m_attackers_ids.begin(), m_attackers_ids.end(), attacker_id);
	if (position != m_attackers_ids.end())
		m_attackers_ids.erase(position);
}

int Target::getNextId()
{
	s_next_id++;
	return s_next_id;
}

int Target::MinTakeOver(const Creature creature, const int number)
{
	if (creature == Humans) {
		return number;
	}
	return ceil(1.5 * number);
}
