#ifndef ATTACKER_H_INCLUDED 
#define ATTACKER_H_INCLUDED 

#include <vector>
#include <map>
#include <algorithm>

class Target;
class Attacker
{
public:	
	Attacker(const int x, const int y, const int number);
	void udpate(int number);
	void updateTargets(std::map<int, Target>& targets_map);
	void addTarget(const int target_id);
	void removeTarget(const int target_id);

	static int getNextId();

private:
	static int s_next_id;
	const int m_id;
	const int m_x;
	const int m_y;
	int m_number;
	std::vector<int> m_targets_ids;
};

#endif

