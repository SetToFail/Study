test_cases = [
    (500, 8),
    (600, 10),
    (750, 7),
    (800, 5)
]
for stavka, hours in test_cases:
    zp = stavka * hours
    print(f"Зарплата: {int(zp)} руб.")