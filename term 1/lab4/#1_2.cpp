#include <iostream>
#include <fstream>
#include <string>
#include <chrono>
#include <Windows.h>
using namespace std;
using namespace chrono;
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
    long long count = 0;
    string line;
    auto start = high_resolution_clock::now();
    while (getline(inputFile, line)) {
        size_t pos = line.find(pattern);
        while (pos != string::npos) {
            count++;
            pos = line.find(pattern, pos + 1); 
        }
    }
    auto end = high_resolution_clock::now();
    auto duration = duration_cast<microseconds>(end - start);
    inputFile.close();
    cout << "Количество повторений подстроки: " << count << endl;
    cout << "Время выполнения: " << duration.count() << " микросекунд" << endl;
    return 0;
}