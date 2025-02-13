import random
size = int(input("Введите размер массива: "))
num = int(input("Введите число, для проверки кратности: "))
arr = [random.randint(1, 100) for _ in range(size)]
count = sum(1 for x in arr if x % num == 0)
print(f"Сгенерированный массив: {arr}")
print(f"Количество элементов, кратных {num}: {count}")