#include <iostream>
#include <regex>
#include <string>
#include <cstdlib>
using namespace std;
int main()
{
    setlocale(LC_ALL, "");
    string text;
    cout << "Введите строку: ";
    getline(cin, text);
    regex pattern("\\b[A-Z]+[\\w]*\\b");
    smatch match;
    cout << "Слова, начинающиеся с заглавной буквы:" << endl;
    while (regex_search(text, match, pattern))
    {
        cout << match[0] << endl;
        text = match.suffix().str();
    }
    return 0;
}