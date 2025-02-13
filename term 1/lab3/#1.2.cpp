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
    int mass[n];
    for (int i = 0; i < n; i++)
    {
        mass[i] = rand() % 11;
        cout << i + 1 << '.' << mass[i] << endl;
    }
    for (int i = 0; i < n - 1; i++)
    {
        int minInd = i;
        for (int j = i + 1; j < n; j++)
        {
            if (mass[j] < mass[minInd])
            {
                minInd = j;
            }
        }
        if (minInd != i)
        {
            swap(mass[i], mass[minInd]);
        }
    }
    cout << "Отсортированный массив: " << endl;
    for (int i = 0; i < n; i++)
    {
        cout << mass[i] << endl;
    }
    system("pause");
    return 0;
}