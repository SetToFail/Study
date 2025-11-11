test_cases = [
    (56, 98),
    (24, 36),
    (21, 14),
    (81, 153)
]
for a, b in test_cases:
    while b != 0:
        a, b = b, a % b
    print(f"НОД: {a}")