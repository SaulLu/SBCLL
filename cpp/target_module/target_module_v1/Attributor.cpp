#include "Attributor.h"

using namespace std;

Attributor::Attributor(const map<Creature, vector<array<int, 3>>> creatures, const Creature player)
{
	m_creatures = creatures;
	m_player = player;
	constructTA();
}

vector<Attributions> Attributor::getTargetAttribution()
{
	/*Attributions attributions;
	auto it = m_attackers.begin();
	auto it2 = m_attackers.begin(); it2++;
	attributions.second.push_back(Attribution(it->second, it2->second, it->second.getNumber()));
	attributions.second.push_back(Attribution(it2->second, it->second, it2->second.getNumber()));
	return { attributions };*/
	Attributions empty_attributions;
	return recursiveTargetAttribution(empty_attributions, m_attackers, m_targets);

}

void Attributor::constructTA()
{
	for (auto& unit : m_creatures[m_player])
	{
		int new_id = Attacker::getNextId();
		m_attackers.insert(make_pair(new_id, Attacker({ unit[0], unit[1] }, unit[2], new_id)));
	}


	for (auto& unit : m_creatures[Creature::Humans])
	{
		int new_id = Target::getNextId();
		m_targets.insert(make_pair(new_id, Target({ unit[0], unit[1] }, Creature::Humans, unit[2], new_id)));
	}

	Creature enemy = m_player == Creature::Us ? Creature::Them : Creature::Us;

	for (auto& unit : m_creatures[enemy])
	{
		int new_id = Target::getNextId();
		m_targets.insert(make_pair(new_id, Target({ unit[0], unit[1] }, enemy, unit[2], new_id)));
	}

	//set attackers and targets attributes
	for (auto& attacker_obj : m_attackers)
	{
		for (auto& target_obj : m_targets)
		{
			if (attacker_obj.second.getNumber() >= target_obj.second.getTakeOver())
			{
				attacker_obj.second.addTarget(target_obj.first);
				target_obj.second.addAttacker(attacker_obj.first);
			}
		}
	}

}

vector<Attributions> Attributor::recursiveTargetAttribution(Attributions current_attribution, map<int, Attacker> attackers, map<int, Target> targets)
{
	int target_id = getNextTargetId(targets);
	if (target_id > 0)
	{
		if (target_id == 3)
			int trash = 0;
		vector<Attributions> all_attributions;
		int takeover = targets[target_id].getTakeOver();
		bool infer = false;

		const vector<int>* target_attackers_p = targets[target_id].getAttackersIdsPointer();
		for (auto& attacker_id : *target_attackers_p)
		{
			Attacker& attacker = attackers[attacker_id];
			int min_takeovers = attacker.getMinTakeOvers(targets, target_id);

			int attacker_number = attacker.getNumber();
			int max_partial_attribution = attacker_number - min_takeovers;

			vector<int> creature_numbers = { attacker_number };
			if (min_takeovers)
			{
				for (int n = takeover; n <= max_partial_attribution; n++)
					creature_numbers.push_back(n);
			}

			for (auto& number_sent : creature_numbers)
			{
				vector<Attributions> new_attributions = applyAttribution(current_attribution, attackers, targets, target_id,
																			attacker_id, number_sent, infer);
				all_attributions.insert(all_attributions.end(), new_attributions.begin(), new_attributions.end());
			}
		}

		if (infer) //need to ignore this target at least once
		{
			vector<Attributions> new_attributions = applyAttribution(current_attribution, attackers, targets, target_id, -1, 0, infer);
			all_attributions.insert(all_attributions.end(), new_attributions.begin(), new_attributions.end());
		}

		return all_attributions;
	}
	else
	{
		if (Checks::checkAttributions(current_attribution, m_attackers, m_targets) != TargetError::noError)
			return {};
		applyMergeAttribution(current_attribution, attackers);
		if (current_attribution.first.size() + current_attribution.second.size() == 0) // alone and outnumbered
			applySuicidalAttribution(current_attribution, attackers, targets);
		return { current_attribution };
	}
}

vector<Attributions> Attributor::applyAttribution(Attributions current_attributions, map<int, Attacker> attackers, map<int, Target> targets, const int target_id, const int attacker_id, const int number_sent, bool& infer)
{
	if (number_sent == 3 && target_id == 1 && attacker_id == 1)
		int trash = 1;

	if (number_sent) //si un envoie est effectu� (envoi nul => ignorer la target)
	{
		current_attributions.first.push_back(Attribution(attackers[attacker_id], targets[target_id], number_sent));
		attackers[attacker_id].lowerNumber(number_sent);
		attackers[attacker_id].removeTarget(target_id, targets, attackers);
		infer = attackers[attacker_id].updateTargets(targets, attackers) || infer;
	}

	targets[target_id].clearAttackers();

	for (auto& attacker : attackers)
	{
		attacker.second.removeTarget(target_id, targets, attackers);
	}

	return recursiveTargetAttribution(current_attributions, attackers, targets);
}

const int Attributor::getNextTargetId(map<int, Target> targets)
{
	for (auto& target_obj : targets)
	{
		const vector<int>* target_attackers_p = target_obj.second.getAttackersIdsPointer();
		if (target_attackers_p->size())
		{
			return target_obj.first;
		}
	}
	return -1;
}

const int Attributor::getClosestAlly(const int attacker_id)
{
	array<int, 2> location = m_attackers[attacker_id].getLocation();
	int closest_ally = -1;
	int best_dist = INT_MAX;

	for (auto& attacker : m_attackers)
	{
		if (attacker.first != attacker_id)
		{
			array<int, 2> location2 = attacker.second.getLocation();
			int dist = max(abs(location[0] - location2[0]), abs(location[1] - location2[1]));
			if (dist < best_dist)
			{
				best_dist = dist;
				closest_ally = attacker.first;
			}
		}
	}

	return closest_ally;
}

void Attributor::applyMergeAttribution(Attributions& current_attributions, std::map<int, Attacker>& attackers)
{
	for (auto& attacker : attackers)
	{
		int attacker_number = attacker.second.getNumber();
		if (attacker_number)
		{
			int closest_ally_id = getClosestAlly(attacker.first);
			if (closest_ally_id > 0)
				current_attributions.second.push_back(Attribution(attacker.second, attackers[closest_ally_id], attacker_number));
		}
	}
}

void Attributor::applySuicidalAttribution(Attributions& current_attributions, std::map<int, Attacker>& attackers, std::map<int, Target>& targets)
{
	int best_target_id = -1;
	int best_takeover = INT_MAX;

	for (auto& target_obj : targets)
	{
		int takeover = target_obj.second.getTakeOver();
		if (takeover < best_takeover)
		{
			best_takeover = takeover;
			best_target_id = target_obj.first;
		}
	}

	auto it = attackers.begin();
	current_attributions.first.push_back(Attribution(it->second, targets[best_target_id], it->second.getNumber()));

}


