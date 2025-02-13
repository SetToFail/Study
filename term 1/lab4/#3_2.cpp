#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <chrono>
#include <unordered_map>
#include <Windows.h>
using namespace std;
using namespace chrono;
unordered_map<char, int> buildShiftTable(const string& pattern) {
    unordered_map<char, int> shiftTable;
    int m = pattern.length();
    for (int i = 0; i < m - 1; ++i) {
        shiftTable[pattern[i]] = m - 1 - i;
    }
    return shiftTable;
}
long long boyerMooreHorspool(const string& text, const string& pattern) {
    int n = text.length();
    int m = pattern.length();
    long long count = 0;
    unordered_map<char, int> shiftTable = buildShiftTable(pattern);
    int i = m - 1;
    while (i < n) {
        int k = 0;
        while (k < m && pattern[m - 1 - k] == text[i - k]) {
            k++;
        }
        if (k == m) {
            count++;
        }
        i += shiftTable.count(text[i]) ? shiftTable[text[i]] : m;
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
    string line;
    long long totalCount = 0;
    auto start = high_resolution_clock::now();
    while (getline(inputFile, line)) {
        totalCount += boyerMooreHorspool(line, pattern);
    }
    auto end = high_resolution_clock::now();
    auto duration = duration_cast<microseconds>(end - start);
    inputFile.close();
    cout << "Количество вхождений: " << totalCount << endl;
    cout << "Время выполнения: " << duration.count() << " микросекунд" << endl;
    return 0;
}