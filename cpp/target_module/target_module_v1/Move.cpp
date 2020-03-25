#include "Move.h"

Move::Move(const std::array<int, 2> start, const int number, const std::array<int, 2> arrival): m_start(start), m_number(number), m_arrival(arrival)
{

}

std::array<int, 2> Move::getStart()
{
	return m_start;
}

std::array<int, 2> Move::getArrival()
{
	return m_arrival;
}

int Move::getNumber()
{
	return m_number;
}
