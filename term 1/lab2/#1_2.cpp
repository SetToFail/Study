#include <iostream>
#include <string>
using namespace std;
int main()
{
    setlocale(LC_ALL, "");
    wstring str, big, smal;
    getline(wcin, str);
    int n = str.length(), count = 0;
    for (int i = 0; n > i; ++i)
    {
        if (str[i] == L'а' || str[i] == L'А' ||
            str[i] == L'о' || str[i] == L'О' ||
            str[i] == L'у' || str[i] == L'У' ||
            str[i] == L'э' || str[i] == L'Э' ||
            str[i] == L'ы' || str[i] == L'Ы' ||
            str[i] == L'я' || str[i] == L'Я' ||
            str[i] == L'е' || str[i] == L'Е' ||
            str[i] == L'ё' || str[i] == L'Ё' ||
            str[i] == L'ю' || str[i] == L'Ю' ||
            str[i] == L'и' || str[i] == L'И')
        {
            count++;
        }
    }
    cout << "Гласных букв: " << count << '\n';
    system("pause");
    return 0;
}