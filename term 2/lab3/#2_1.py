total_cost = 0.0
try:
    with open('prices.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()
        if not lines:
            print("0.00")
        else:
            for line in lines:
                columns = line.strip().split('\t')
                if len(columns) == 3:
                    name, quantity, price = columns
                    try:
                        quantity = int(quantity)
                        price = float(price)
                        total_cost += quantity * price
                    except ValueError:
                        continue
            print(f"{total_cost:.2f}")
except FileNotFoundError:
    print("File prices.txt not found.")
except Exception as e:
    print(f"Error: {e}")