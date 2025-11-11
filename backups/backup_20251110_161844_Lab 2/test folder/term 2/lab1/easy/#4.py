arr = list(map(int, input("Введите массив целых чисел: ").split()))
max_index = arr.index(max(arr))
min_index = arr.index(min(arr))
start = min(max_index, min_index) + 1
end = max(max_index, min_index)
if start >= end:
    print("Между максимальным и минимальным элементами нет других элементов.")
else:
    max_between = max(arr[start:end])
    print(f"Максимальный элемент между максимальным и минимальным: {max_between}")