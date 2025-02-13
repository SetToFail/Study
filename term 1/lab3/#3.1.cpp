#include <iostream>
#include <string>
#include <sstream>
#include <vector>
#include <limits>
#include <cmath>
using namespace std;
int partition(vector<int> &mass, int low, int high)
{
    int opor = mass[high];
    int i = (low - 1);
    for (int j = low; j <= high - 1; j++)
    {
        if (mass[j] <= opor)
        {
            i++;
            swap(mass[i], mass[j]);
        }
    }
    swap(mass[i + 1], mass[high]);
    return (i + 1);
}
void quickSort(vector<int> &mass, int low, int high)
{
    if (low < high)
    {
        int opor = partition(mass, low, high);
        quickSort(mass, low, opor - 1);
        quickSort(mass, opor + 1, high);
    }
}
int main()
{
    int n;
    cout << "Размер массива: ";
    cin >> n;
    vector<int> mass(n, 0);
    for (int i = 0; i < n; i++)
    {
        mass[i] = rand() % 101;
        cout << i + 1 << '.' << mass[i] << endl;
    }
    cout << endl;
    quickSort(mass, 0, n - 1);
    cout << "Отсортированный массив: \n";
    for (int i = 0; i < n; i++)
    {
        cout << mass[i] << endl;
    }
    cout << endl;
    return 0;
}