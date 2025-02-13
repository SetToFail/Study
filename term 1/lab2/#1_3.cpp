#include <iostream>
#include <string>
#include <sstream>
#include <vector>
#include <cmath>
using namespace std;
int main()
{
    setlocale(LC_ALL, "");
    int x, count, countb, i, y = INFINITY;
    wstring str, big, small;
    getline(wcin, str);
    wistringstream iss(str);
    vector<wstring> words;
    for (wstring word; iss >> word;)
    {
        if (word.size() >= x)
        {
            x = word.size();
            count = i;
            big = word;
        }
        if (word.size() <= y)
        {
            y = word.size();
            countb = i;
            small = word;
        }
        ++i;
    }
    if (count < countb)
    {
        wcout << L"Ближе к концу строки максимальной длины слово: " << big << endl;
    }
    else
    {
        wcout << L"Ближе к концу строки минимальной длины слово: " << small << endl;
    }
    system("pause");
    return 0;
}