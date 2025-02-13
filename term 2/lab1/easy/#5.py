s = input("Введите строку: ")
vowels = "аеёиоуыэюяАЕЁИОУЫЭЮЯaeiouAEIOU"
count = sum(1 for char in s if char in vowels)
print(f"Количество гласных букв в строке: {count}")