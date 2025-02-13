#include <Windows.h>
#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <chrono>
#include <limits>
using namespace std;
using namespace chrono;
vector<int> prefixFunction(const string& pattern) {
    int m = pattern.length();
    if (m == 0) return {};
    vector<int> pi(m, 0);
    int k = 0;
    for (int q = 1; q < m; ++q) {
        while (k > 0 && pattern[k] != pattern[q]) {
            k = pi[k - 1];
        }
        if (pattern[k] == pattern[q]) {
            k++;
        }
        pi[q] = k;
    }
    return pi;
}
long long knuthMorrisPratt(const string& text, const string& pattern) {
    if (pattern.empty()) return 0;
    vector<int> pi = prefixFunction(pattern);
    int n = text.length();
    int m = pattern.length();
    long long count = 0;
    int q = 0;
    for (int i = 0; i < n; ++i) {
        while (q > 0 && pattern[q] != text[i]) {
            q = pi[q - 1];
        }
        if (pattern[q] == text[i]) {
            q++;
        }
        if (q == m) {
            count++;
            q = pi[q - 1];
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
    cin >> filePath;
    cin.ignore(numeric_limits<streamsize>::max(), '\n'); 
    cout << "Введите искомую подстроку: ";
    getline(cin, pattern);
    ifstream inputFile(filePath, ios::binary); 
    if (!inputFile.is_open()) {
        cerr << "Ошибка открытия файла!" << endl;
        return 1;
    }
    inputFile.seekg(0, ios::end);
    long long fileSize = inputFile.tellg();
    inputFile.seekg(0, ios::beg);
    string text;
    text.resize(fileSize);
    inputFile.read(&text[0], fileSize);
    inputFile.close();
    auto start = high_resolution_clock::now();
    long long totalCount = knuthMorrisPratt(text, pattern);
    auto end = high_resolution_clock::now();
    auto duration = duration_cast<microseconds>(end - start);
    cout << "Количество вхождений: " << totalCount << endl;
    cout << "Время выполнения: " << duration.count() << " микросекунд" << endl;
    return 0;
}