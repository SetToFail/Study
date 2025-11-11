import math
test_cases = [
    (0, 0, 0, 1),
    (1, 1, 4, 5),
    (-1, -1, 1, 1),
    (2, 2, 2, 2)
]
for x1, y1, x2, y2 in test_cases:
    result = round(math.sqrt((x2 - x1)**2 + (y2 - y1)**2), 2)
    print(f"Расстояние между точками ({x1}, {y1}) и ({x2}, {y2}) равно {result}")