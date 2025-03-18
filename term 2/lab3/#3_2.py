import openpyxl
import csv
wb = openpyxl.load_workbook(filename='data.xlsx', data_only=True)
sheet = wb.active
with open('output.csv', 'w', encoding='cp1251', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=';', quoting=csv.QUOTE_ALL)
    for row in sheet.iter_rows(values_only=True):
        writer.writerow(row)