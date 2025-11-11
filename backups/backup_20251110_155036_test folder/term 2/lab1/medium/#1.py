import math
test_cases = [
    (1, -3, 2),
    (1, 2, 1),
    (1, 0, -1),
    (1, 2, 5)
]
for a, b, c in test_cases:
    if a == 0:
        print("Это не квадратное уравнение (a не может быть равно 0).")
    else:
        discriminant = b**2 - 4*a*c
        if discriminant > 0:
            x1 = (-b + math.sqrt(discriminant)) / (2*a)
            x2 = (-b - math.sqrt(discriminant)) / (2*a)
            print(f"Корни: x1={round(x1, 2)}, x2={round(x2, 2)}")
        elif discriminant == 0:
            x1 = -b / (2*a)
            print(f"Корень: x1={round(x1, 2)}")
        else:
            print("Нет действительных корней.")
