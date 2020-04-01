#include "Target.h"
#include "Attacker.h"

using namespace std;

int Target::s_next_id = 0;

Target::Target() 
	: m_location({ -1, -1 }), m_creature(Creature::Empty), m_number(-1), m_takeover(-1), m_id(-1)
{

}

Target::Target(const std::array<int, 2> location, const Creature creature, const int number, const int id)
		: m_location(location), m_creature(creature), m_number(number), m_takeover(computeTakeOver(creature, number)), m_id(id)
{

}

const int Target::getNumber()
{
	return m_number;
}

const int Target::getTakeOver()
{
	return m_takeover;
}

void Target::addAttacker(const int attacker_id)
{
	m_attackers_ids.push_back(attacker_id);
}

bool Target::removeAttacker(const int attacker_id)
{
	vector<int>::iterator position = find(m_attackers_ids.begin(), m_attackers_ids.end(), attacker_id);
	if (position != m_attackers_ids.end())
	{
		m_attackers_ids.erase(position);
		return m_attackers_ids.size() == 0;
	}
		
	return false;
}

void Target::purgeAttackers(std::map<int, Target>& targets, std::map<int, Attacker>& attackers)
{
	int k = 0;
	while (k < m_attackers_ids.size())
	{
		int attacker_id = m_attackers_ids[k];
		if (attackers[attacker_id].getNTargets() > 1)
		{
			m_attackers_ids.erase(m_attackers_ids.begin() + k);
			attackers[attacker_id].removeTarget(m_id, targets, attackers);
		}
		else 
		{
			k++;
		}
	}
}

void Target::clearAttackers()
{
	m_attackers_ids.clear();
}

const std::array<int, 2> Target::getLocation()
{
	return m_location;
}

int Target::getNextId()
{
	s_next_id++;
	return s_next_id;
}

const std::vector<int>* Target::getAttackersIdsPointer()
{
	return &m_attackers_ids;
}

Target Target::operator=(const Target& t)
{
	return Target(t.m_location, t.m_creature, t.m_number, t.m_id);
}

int Target::computeTakeOver(const Creature creature, const int number)
{
	if (creature == Creature::Humans) {
		return number;
	}
	return (int)ceil(1.5 * number);
}
