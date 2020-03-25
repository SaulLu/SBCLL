#include "Attacker.h"
#include "Target.h"

using namespace std;

int Attacker::s_next_id = -1;

Attacker::Attacker(const int x, const int y, const int number) : m_x(x), m_y(y), m_number(number), m_id(getNextId())
{
}

void Attacker::udpate(int number)
{
	m_number = number;
}

void Attacker::updateTargets(std::map<int, Target>& targets_map)
{
	auto vector_begin = m_targets_ids.begin();
	int n_targets = m_targets_ids.size();
	int k = 0;
	while (k < n_targets) {
		int target_id = m_targets_ids[k];
		if (targets_map[target_id].getMinTakeOver() > m_number) {
			m_targets_ids.erase(vector_begin + k);
			n_targets--;
			targets_map[target_id].removeAttacker(m_id);
		}
		else
		{
			k++;
		}
	}
}

void Attacker::addTarget(const int target_id)
{
	m_targets_ids.push_back(target_id);
}

void Attacker::removeTarget(const int target_id)
{
	vector<int>::iterator position = find(m_targets_ids.begin(), m_targets_ids.end(), target_id);
	if (position != m_targets_ids.end())
		m_targets_ids.erase(position);
}

int Attacker::getNextId()
{
	s_next_id++;
	return s_next_id;
}

