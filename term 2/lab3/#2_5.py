import csv
try:
    with open('wares2.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file, delimiter=';')
        for row in reader:
            try:
                old_price = int(row['Old price'])
                new_price = int(row['New price'])             
                if new_price < old_price:
                    print(row['Name'])
            except (ValueError, KeyError):
                continue
except FileNotFoundError:
    print("File wares.csv not found.")
except Exception as e:
    print(f"Error: {e}")