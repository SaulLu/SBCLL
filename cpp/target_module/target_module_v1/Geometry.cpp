#include "Geometry.h"

using namespace std;

const double PI = 3.1415;

double Geometry::getSeparationAngle(const array<int, 2> center, const array<int, 2> pos1, const array<int, 2> pos2)
{
	array<int, 2> v1 = getVector(center, pos1);
	array<int, 2> v2 = getVector(center, pos2);
	return getDegreeAngle(v1, v2);
}

double Geometry::getDegreeAngle(const array<int, 2> v1, const array<int, 2> v2)
{
	return acos(getDotProduct(v1, v2) / (getNorme(v1) * getNorme(v2))) * 180 / PI;
}

double Geometry::getNorme(const array<int, 2> v)
{
	return sqrt(getDotProduct(v, v));
}

double Geometry::getDotProduct(const array<int, 2> v1, const array<int, 2> v2)
{
	return (v1[0] * v2[0]) + (v1[1] * v2[1]);
}

array<int, 2> Geometry::getVector(const array<int, 2> pos1, const array<int, 2> pos2)
{
	return { pos2[0] - pos1[0], pos2[1] - pos1[1] };
}

int Geometry::getMovementDistance(const array<int, 2> pos1, const array<int, 2> pos2)
{
	return max(abs(pos2[0] - pos1[0]), abs(pos2[1] - pos1[1]));
}
