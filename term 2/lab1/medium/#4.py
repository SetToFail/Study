import random
n = int(input("Введите размер массива: "))
arr = [random.randint(2, 100) for _ in range(n)]
print("Сгенерированный массив:", arr)
sum_even_positions = sum(arr[i] for i in range(1, n, 2))
print(f"Сумма элементов на чётных позициях: {sum_even_positions}")
