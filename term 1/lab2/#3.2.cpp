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
    int n, count;
    cout << "Размер массива: ";
    cin >> n;
    int mass[n];
    for (int i = 0; i < n; i++)
    {
        mass[i] = rand() % 11;
        cout << i + 1 << '.' << mass[i] << endl;
    }
    for (int i = 0; i < n; i++)
    {
        for (int j = 0; j < n - 1; j++)
        {
            if (mass[j] > mass[j + 1])
            {
                int a = mass[j];
                mass[j] = mass[j + 1];
                mass[j + 1] = a;
            }
        }
    }
    cout << "Отсортированный массив: " << endl;
    for (int i = 0; i < n; i++)
    {
        cout << i + 1 << "." << mass[i] << endl;
    }
    count = n / 2;
    if (n % 2 == 0)
    {
        cout << "Медиана: (" << mass[count - 1] <<  " + " << mass[count] << ") / 2 = " << (mass[count - 1] + mass[count]) / 2 << endl;
    }
    else
    {
        cout << "Медиана: " << mass[count] << endl;
    }
    system("pause");
    return 0;
}