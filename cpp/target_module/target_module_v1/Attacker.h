#ifndef ATTACKER_H_INCLUDED 
#define ATTACKER_H_INCLUDED 

#include <array>
#include <vector>
#include <map>
#include <algorithm>
#include <limits.h>

class Target;
class Attacker
{
public:	
	Attacker();
	Attacker(const std::array<int,2> location, const int number, const int id);
	void lowerNumber(int number_sent);
	bool updateTargets(std::map<int, Target>& targets, std::map<int, Attacker>& attackers);
	void addTarget(const int target_id);
	void removeTarget(const int target_id, std::map<int, Target>& targets, std::map<int, Attacker>& attackers);
	const int getId();
	const int getNumber();
	const int getNTargets();
	const std::array<int, 2> getLocation();
	const int getMinTakeOvers(std::map<int, Target>& targets, int id_to_exlud = -1);

	static int getNextId();

	Attacker operator=(const Attacker& a);

private:
	static int s_next_id;
	const int m_id;
	const std::array<int, 2> m_location;
	int m_number;
	std::vector<int> m_targets_ids;
};

#endif

