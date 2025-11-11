s = input("Введите строку: ")
words = s.split()
max_word = max(words, key=len)
min_word = min(words, key=len)
max_index = len(words) - words[::-1].index(max_word) - 1
min_index = len(words) - words[::-1].index(min_word) - 1
if max_index > min_index:
    print(f"Слово максимальной длины '{max_word}' ближе к концу строки.")
else:
    print(f"Слово минимальной длины '{min_word}' ближе к концу строки.")