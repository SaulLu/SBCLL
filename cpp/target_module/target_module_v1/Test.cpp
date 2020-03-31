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

	Attributor attributor = Attributor(creatures, player, 20, 20);

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

	Attributor attributor = Attributor(creatures, player, 20, 20);

	vector<Attributions> all_attributions = attributor.getTargetAttribution();

	return all_attributions;
}

vector<Attributions> Test::testViableTargets3()
{
	Creature player = Creature::Us;
	map<Creature, vector<array<int, 3>>> creatures;

	creatures[Creature::Us].push_back({ 4, 1, 10 });
	creatures[Creature::Us].push_back({ 5, 0, 11 });

	creatures[Creature::Them].push_back({ 1, 7 ,19 });
	creatures[Creature::Them].push_back({ 6, 2 ,6 });

	Attributor attributor = Attributor(creatures, player, 20, 20, 22.5, 1.95);

	vector<Attributions> all_attributions = attributor.getTargetAttribution();

	return all_attributions;
}

vector<Attributions> Test::testViableTargets4()
{
	Creature player = Creature::Them;
	vector<array<int, 4>> creatures_vector = { {{5, 1, 1, 11}, {1, 7, 2, 19}, {6, 2, 2, 6}} };

	map<Creature, vector<array<int, 3>>> creatures;

	for (auto& creature : creatures_vector)
	{
		switch (creature[2])
		{
		case 0:
			creatures[Creature::Humans].push_back({ creature[0], creature[1], creature[3] });
			break;
		case 1:
			creatures[Creature::Us].push_back({ creature[0], creature[1], creature[3] });
			break;
		case 2:
			creatures[Creature::Them].push_back({ creature[0], creature[1], creature[3] });
			break;
		default:
			break;
		}
	}

	Attributor attributor = Attributor(creatures, player, 20, 20, 22.5, 5);

	vector<Attributions> all_attributions = attributor.getTargetAttribution();

	return all_attributions;
}

vector<Attributions> Test::testViableTargets5()
{
	Creature player = Creature::Them;
	map<Creature, vector<array<int, 3>>> creatures;

	creatures[Creature::Us].push_back({ 5, 1, 11 });

	creatures[Creature::Them].push_back({ 1, 7 ,19 });
	creatures[Creature::Them].push_back({ 6, 2 ,6 });

	Attributor attributor = Attributor(creatures, player, 20, 20, 22.5);

	vector<Attributions> all_attributions = attributor.getTargetAttribution();

	return all_attributions;
}

vector<Attributions> Test::testViableTargets6()
{
	Creature player = Creature::Us;
	map<Creature, vector<array<int, 3>>> creatures;

	creatures[Creature::Us].push_back({ 0, 0, 10 });

	creatures[Creature::Them].push_back({ 0, 1 ,11 });

	Attributor attributor = Attributor(creatures, player, 20, 20, 22.5);

	vector<Attributions> all_attributions = attributor.getTargetAttribution();

	return all_attributions;
}