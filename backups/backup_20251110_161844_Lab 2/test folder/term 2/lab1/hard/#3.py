s = input("Введите строку: ")
words = s.split()
result = [word for word in words if word[0].isupper()]
print(f"Слова, начинающиеся с заглавной буквы: {', '.join(result)}")