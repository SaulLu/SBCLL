#include "Test.h"

using namespace std;

vector<Attributions> Test::testViableTargets()
{
	Creature player = Creature::Us;
	map<Creature, vector<array<int, 3>>> creatures;

	creatures[Creature::Humans].push_back({ 2, 5, 1 });
	creatures[Creature::Humans].push_back({4, 5, 2});

	creatures[Creature::Us].push_back({ 3, 6, 3 });
	creatures[Creature::Us].push_back({ 3, 5, 8 });
	creatures[Creature::Us].push_back({ 1, 10, 8 });
	creatures[Creature::Us].push_back({ 3, 25, 8 });

	creatures[Creature::Them].push_back({ 7, 7, 3 });
	creatures[Creature::Them].push_back({ 19, 7, 5 });

	Attributor attributor = Attributor(creatures, player);

	vector<Attributions> all_attributions = attributor.getTargetAttribution();

	return all_attributions;
}

vector<Attributions> Test::testViableTargets2()
{
	Creature player = Creature::Us;
	map<Creature, vector<array<int, 3>>> creatures;

	creatures[Creature::Humans].push_back({ 2, 5, 8});

	creatures[Creature::Us].push_back({ 3, 6, 4});

	creatures[Creature::Them].push_back({ 4, 5 ,8});

	Attributor attributor = Attributor(creatures, player);

	vector<Attributions> all_attributions = attributor.getTargetAttribution();

	return all_attributions;
}

vector<Attributions> Test::testViableTargets3()
{
	Creature player = Creature::Us;
	map<Creature, vector<array<int, 3>>> creatures;

	creatures[Creature::Us].push_back({ 2, 2, 2 });
	creatures[Creature::Us].push_back({ 3, 3, 2 });

	creatures[Creature::Them].push_back({ 4, 4 ,2 });
	creatures[Creature::Them].push_back({ 5, 3 ,2 });

	Attributor attributor = Attributor(creatures, player);

	vector<Attributions> all_attributions = attributor.getTargetAttribution();

	return all_attributions;
}
