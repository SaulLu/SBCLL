#ifndef ENUMS_H_INCLUDED 
#define ENUMS_H_INCLUDED 

enum class Creature : int
{
	Empty = 0,
	Humans = 1,
	Us = 2,
	Them = 3
};

enum class TargetError : int
{
	noError = 0,
	LeftOver = 1,
	OverSend = 2,
	MissedOpportunity = 3,
	OverTargeted = 4,
	UnderTargeted = 5
};


#endif
