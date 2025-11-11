test_cases = [
    (8, 2),
    (16, 1),
    (32, 4),
    (4, 1)   
]
for start, end in test_cases:
    count = 0
    while start > end:
        start /= 2
        count += 1
    print(f"Прокаток: {count}")