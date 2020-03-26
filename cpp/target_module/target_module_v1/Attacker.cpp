#include "Attacker.h"
#include "Target.h"

using namespace std;

int Attacker::s_next_id = 0;

Attacker::Attacker() : m_location({ NULL, NULL }), m_number(NULL), m_id(NULL)
{

}

Attacker::Attacker(const std::array<int, 2> location, const int number, const int id) : m_location(location), m_number(number), m_id(id)
{
}

void Attacker::lowerNumber(int number_sent)
{
	m_number -= number_sent;
}

bool Attacker::updateTargets(std::map<int, Target>& targets, std::map<int, Attacker>& attackers)
{
	bool infer = false;
	int n_targets = m_targets_ids.size();
	int k = 0;
	while (k < n_targets) {
		int target_id = m_targets_ids[k];
		if (targets[target_id].getTakeOver() > m_number) {
			m_targets_ids.erase(m_targets_ids.begin() + k);
			n_targets--;
			infer = infer || targets[target_id].removeAttacker(m_id);
		}
		else
		{
			k++;
		}
	}

	if (m_targets_ids.size() == 1)
	{
		targets[m_targets_ids[0]].purgeAttackers(targets, attackers);
	}

	return infer;
}

void Attacker::addTarget(const int target_id)
{
	m_targets_ids.push_back(target_id);
}

void Attacker::removeTarget(const int target_id, std::map<int, Target>& targets, std::map<int, Attacker>& attackers)
{
	vector<int>::iterator position = find(m_targets_ids.begin(), m_targets_ids.end(), target_id);
	if (position != m_targets_ids.end())
	{
		m_targets_ids.erase(position);

		if (m_targets_ids.size() == 1)
		{
			targets[target_id].purgeAttackers(targets, attackers);
		}
	}
		
}

const int Attacker::getId()
{
	return m_id;
}

const int Attacker::getNumber()
{
	return m_number;
}

const int Attacker::getNTargets()
{
	return m_targets_ids.size();
}

const std::array<int, 2> Attacker::getLocation()
{
	return m_location;
}

const int Attacker::getMinTakeOvers(std::map<int, Target>& targets, int id_to_exclude)
{
	int min_takerovers = INT_MAX;
	for (auto& target_id : m_targets_ids)
	{
		if (target_id != id_to_exclude)
		{
			int temp_takeover = targets[target_id].getTakeOver();
			if (temp_takeover < min_takerovers)
			{
				min_takerovers = temp_takeover;
			}
		}
	}

	if (min_takerovers == INT_MAX) return 0;

	return min_takerovers;
}

int Attacker::getNextId()
{
	s_next_id++;
	return s_next_id;
}

Attacker Attacker::operator=(const Attacker& a)
{
	return Attacker(a.m_location, a.m_number, a.m_id);
}
