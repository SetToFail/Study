#include <iostream>
#include <string>
#include <sstream>
#include <vector>
#include <limits>
#include <cmath>
using namespace std;
int main()
{
    system("chcp 1251");
    int n;
    cout << "Размер массива: ";
    cin >> n;
    double mass[n];
    for (int i = 0; i < n; i++)
    {
        mass[i] = rand() % 101;
        cout << i + 1 << '.' << mass[i] << endl;
    }
    double count = n;
    for (int i = 0; i < n; i++)
    {
        int shag = i + count;
        for (int j = 0; j < n; j++)
        {
            if (mass[j] > mass[shag])
            {
                swap(mass[j], mass[shag]);
            }
        }
        count = floor(count / 2);
        if (count == 0)
        {
            continue;
        }
    }
    cout << "Отсортированный массив: " << endl;
    for (int i = 1; i < n + 1; i++)
    {
        cout << mass[i] << endl;
    }
    system("pause");
    return 0;
}