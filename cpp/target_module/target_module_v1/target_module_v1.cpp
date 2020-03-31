#include <iostream>
#include <vector>

#include "Test.h"

using namespace std;

void printAllAttributions(vector<Attributions>& all_attributions);

int main()
{
    vector<Attributions> all_attributions = Test::testViableTargets2();
    printAllAttributions(all_attributions);
}


void printAllAttributions(vector<Attributions>& all_attributions)
{
    for (auto& attributions : all_attributions)
    {
        cout << "\n";

        cout << "attacks:\n";
        for (auto& attribution : attributions.first)
        {
            cout << "\tstart: (" << attribution.start[0] << ", " << attribution.start[1] << "), (" << attribution.target[0] << ", " << attribution.target[1] << "), " << attribution.number << endl;
        }

        cout << "merges:\n";
        for (auto& attribution : attributions.second)
        {
            cout << "\tstart: (" << attribution.start[0] << ", " << attribution.start[1] << "), (" << attribution.target[0] << ", " << attribution.target[1] << "), " << attribution.number << endl;
        }
    }

    cout << "\n" << all_attributions.size() << " attributions found";
}