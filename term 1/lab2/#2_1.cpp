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
        cout << mass[i] << endl;
    }
    for (int i = 1; i < n - 1; i++)
    {
        sum += mass[i];
    }
    cout << "Сумма без первого и последнего индекса: " << sum << endl;
    system("pause");
    return 0;
}