s = input("Введите строку: ")
words = s.split()
result = [word for word in words if word == word[::-1]]
print(f"Слова-палиндромы: {', '.join(result)}")