#include <iostream>
#include <string>
using namespace std;
int main()
{
    setlocale(LC_ALL, "");
    int mass[]{1, 23, 10, 43, 35, 6 -100};
    int n = sizeof(mass) / sizeof(mass[0]);
    n = size(mass);
    int x = 0, count;
    for (int i = 0; n > i; i++)
    {
        if (mass[i] > x)
        {
            x = mass[i];
            count = i;
        }
    }
    cout << "Самое большое положительное число: " << x << ", под индексом " << count << '\n';
    system("pause");
    return 0;
}