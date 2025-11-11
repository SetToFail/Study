s = input("Введите строку: ")
target = input("Введите заданную подстроку: ")
words = s.split()
result = [word for word in words if target in word]
print(f"Слова, содержащие '{target}': {', '.join(result)}")