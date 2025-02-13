#include <iostream>
using namespace std;
int main()
{
    setlocale(LC_ALL, "");
    int n, sum;
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
        if (i % 2 != 0)
        {
            sum += mass[i];
        }
    }
    cout << "Сумма чисел на чётных позициях: " << sum << endl;
    system("pause");
    return 0;
}