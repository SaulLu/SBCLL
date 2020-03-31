#ifndef GEOMETRY_H_INCLUDED 
#define GEOMETRY_H_INCLUDED

#include <array>
#include <math.h>

class Geometry
{
public:
	static double getSeparationAngle(const std::array<int, 2> center, const std::array<int, 2> pos1, const std::array<int, 2> pos2);
	static double getDegreeAngle(const std::array<int, 2> v1, const std::array<int, 2> v2);
	static double getNorme(const std::array<int, 2> v);
	static double getDotProduct(const std::array<int, 2> v1, const std::array<int, 2> v2);
	static std::array<int,2> getVector(const std::array<int, 2> pos1, const std::array<int, 2> pos2);
	static int getMovementDistance(const std::array<int, 2> pos1, const std::array<int, 2> pos2);
};

#endif