#include "Checks.h"

using namespace std;

TargetError checkAttributions(Attributions attributions, std::map<int, Attacker> attackers, std::map<int, Target> targets);

void Checks::countTargetError(std::vector<Attributions> all_attributions, std::map<int, Attacker> attackers, std::map<int, Target> targets)
{
	map<TargetError, int> errors_count;
	errors_count[TargetError::noError] = 0;
	errors_count[TargetError::LeftOver] = 0;
	errors_count[TargetError::OverSend] = 0;
	errors_count[TargetError::MissedOpportunity] = 0;
	errors_count[TargetError::OverTargeted] = 0;
	errors_count[TargetError::UnderTargeted] = 0;

	for (auto& attributions : all_attributions)
	{
		TargetError error = checkAttributions(attributions, attackers, targets);
		errors_count[error] += 1;
	}

}

TargetError Checks::checkAttributions(Attributions attributions, std::map<int, Attacker> attackers, std::map<int, Target> targets)
{
	map<array<int,2>, int> sent_by_attackers;
	map<array<int, 2>, array<int,2>> attack_on_target;
	for (auto& attribution : attributions.first)
	{
		sent_by_attackers[attribution.start] += attribution.number;
		attack_on_target[attribution.target][0] += 1;
		attack_on_target[attribution.target][1] += attribution.number;
	}

	for (auto& attribution : attributions.second)
	{
		sent_by_attackers[attribution.start] += attribution.number;
	}

	for (auto& attacker : attackers)
	{
		array<int, 2> attacker_location = attacker.second.getLocation();
		int attacker_number = attacker.second.getNumber();

		if (sent_by_attackers[attacker_location] > attacker_number)
		{
			return TargetError::OverSend;
		}
		else if (sent_by_attackers[attacker_location] < attacker_number && sent_by_attackers[attacker_location])
		{
			return TargetError::LeftOver;
		}
	}

	for (auto& target : targets)
	{
		array<int, 2> target_location = target.second.getLocation();
		int takeover = target.second.getTakeOver();

		if (attack_on_target[target_location][0] > 1)
		{
			return TargetError::OverTargeted;
		}
		else if (attack_on_target[target_location][0] == 1)
		{
			if (takeover > attack_on_target[target_location][1])
				return TargetError::UnderTargeted;
		}
		else
		{
			const vector<int>* target_attackers_p = target.second.getAttackersIdsPointer();
			for (auto& target_id : *target_attackers_p)
			{
				array<int, 2> attacker_location = attackers[target_id].getLocation();
				if (sent_by_attackers[attacker_location] == 0)
				{
					return TargetError::MissedOpportunity;
				}
			}
		}
	}



	return TargetError::noError;
}