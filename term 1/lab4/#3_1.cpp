#include <iostream>
#include <fstream>
#include <string>
#include <chrono>
#include <Windows.h>
using namespace std;
using namespace chrono;
unsigned long long simpleHash(const string& str) {
    unsigned long long hash = 0;
    for (char c : str) {
        hash = hash * 31 + c;
    }
    return hash;
}
long long rabinKarpSimple(const string& text, const string& pattern) {
    long long count = 0;
    long long patternHash = simpleHash(pattern);
    for (long long i = 0; i <= (long long)text.length() - (long long)pattern.length(); ++i) {
        if (simpleHash(text.substr(i, pattern.length())) == patternHash && text.substr(i, pattern.length()) == pattern) {
            count++;
        }
    }
    return count;
}
int main() {
    setlocale(LC_ALL, "Russian");
    SetConsoleCP(1251);
    SetConsoleOutputCP(1251);
    string filePath, pattern;
    cout << "Введите путь к файлу: ";
    getline(cin, filePath);
    cout << "Введите искомую подстроку: ";
    getline(cin, pattern);
    ifstream inputFile(filePath);
    if (!inputFile.is_open()) {
        cerr << "Ошибка открытия файла!" << endl;
        return 1;
    }
    string text;
    inputFile.seekg(0, ios::end);
    text.resize(inputFile.tellg());
    inputFile.seekg(0, ios::beg);
    inputFile.read(&text[0], text.size());
    inputFile.close();
    auto start = high_resolution_clock::now();
    long long totalCount = rabinKarpSimple(text, pattern);
    auto end = high_resolution_clock::now();
    auto duration = duration_cast<microseconds>(end - start);
    cout << "Количество вхождений: " << totalCount << endl;
    cout << "Время выполнения: " << duration.count() << " микросекунд" << endl;
    return 0;
}