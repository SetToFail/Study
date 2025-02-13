num = input("Введите число: ")
result = []
for i in range(len(num)):
    digit = num[i]
    if digit == '0':
        continue
    zeros = len(num) - i - 1
    result.append(digit + '0' * zeros)
print(", ".join(result))