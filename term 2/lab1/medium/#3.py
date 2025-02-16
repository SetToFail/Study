import random
n = int(input("Введите размер массива: "))
k = int(input("Введите число, на которое проверяем кратность: "))
arr = [random.randint(1, 100) for _ in range(n)]
print("Сгенерированный массив:", arr)
count = sum(1 for x in arr if x % k == 0)
print(f"Количество элементов, кратных {k}: {count}")
