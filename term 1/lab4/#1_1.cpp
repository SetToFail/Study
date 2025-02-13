#include <Windows.h>
#include <iostream>
#include <fstream>
#include <string>
#include <chrono>
#include <limits> 
using namespace std;
using namespace chrono;
int main() {
    setlocale(LC_ALL, "Russian");
    SetConsoleCP(1251);
    SetConsoleOutputCP(1251);
    string filePath, pattern;
    cout << "������� ���� � �����: ";
    getline(cin, filePath);
    cout << "������� ������� ���������: ";
    getline(cin, pattern);
    ifstream inputFile(filePath);
    if (!inputFile.is_open()) {
        cerr << "������ �������� �����!" << endl;
        return 1;
    }
    long long count = 0;
    string line;
    auto start = high_resolution_clock::now();
    while (getline(inputFile, line)) {
        size_t pos = 0;
        while ((pos = line.find(pattern, pos)) != string::npos) {
            count++;
            pos++;
        }
    }
    auto end = high_resolution_clock::now();
    auto duration = duration_cast<microseconds>(end - start);
    inputFile.close();
    cout << "���������� ���������� ���������: " << count << endl;
    cout << "����� ����������: " << duration.count() << " �����������" << endl;
    return 0;
}