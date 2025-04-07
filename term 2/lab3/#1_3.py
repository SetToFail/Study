import csv
def recommend_purchases():
    budget = 1000
    max_units_per_item = 10
    items = []
    try:
        with open('/home/danina/Repositories/Study/term 2/lab3/wares.csv', 'r', encoding='utf-8') as file:
            reader = csv.reader(file, delimiter=';')
            for row in reader:
                if len(row) == 2:
                    name, price = row[0], int(row[1])
                    items.append((name, price))
    except FileNotFoundError:
        print("error")
        return
    items.sort(key=lambda x: x[1])
    selected_items = []
    remaining_budget = budget
    for name, price in items:
        if price > remaining_budget:
            continue
        max_possible = min(max_units_per_item, remaining_budget // price)
        if max_possible == 0:
            continue
        selected_items.extend([name] * max_possible)
        remaining_budget -= max_possible * price
    if not selected_items:
        print("error")
        return
    output = ", ".join(selected_items)
    print(output)
    with open('/home/danina/Repositories/Study/term 2/lab3/output.txt', 'w', encoding='utf-8') as out_file:
        out_file.write(output)
recommend_purchases()