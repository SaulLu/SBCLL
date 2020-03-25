#ifndef MOVE_H_INCLUDED 
#define MOVE_H_INCLUDED 

#include <array>

class Move
{
public:
	Move(const std::array<int, 2> start, const int number, const std::array<int, 2> arrival);
	std::array<int, 2> getStart();
	std::array<int, 2> getArrival();
	int getNumber();


private:
	const std::array<int, 2> m_start;
	const std::array<int, 2> m_arrival;
	const int m_number;

};

#endif

