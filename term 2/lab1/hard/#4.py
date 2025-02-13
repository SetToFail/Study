s = input("Введите строку: ")
sub = input("Введите подстроку: ")
count = 0
index = 0
while index < len(s):
    index = s.find(sub, index)
    if index == -1:
        break
    count += 1
    index += 1
print(f"Количество вхождений подстроки '{sub}': {count}")