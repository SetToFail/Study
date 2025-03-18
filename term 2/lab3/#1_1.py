translit_table = {
    "й": "j", "ц": "c", "у": "u", "к": "k", "е": "e", "н": "n",
    "г": "g", "ш": "sh", "щ": "shh", "з": "z", "х": "h", "ъ": "#",
    "ф": "f", "ы": "y", "в": "v", "а": "a", "п": "p", "р": "r",
    "о": "o", "л": "l", "д": "d", "ж": "zh", "э": "je", "я": "ya",
    "ч": "ch", "с": "s", "м": "m", "и": "i", "т": "t", "ь": "'",
    "б": "b", "ю": "ju", "ё": "jo",
    
    "Й": "J", "Ц": "C", "У": "U", "К": "K", "Е": "E", "Н": "N",
    "Г": "G", "Ш": "Sh", "Щ": "Shh", "З": "Z", "Х": "H", "Ъ": "#",
    "Ф": "F", "Ы": "Y", "В": "V", "А": "A", "П": "P", "Р": "R",
    "О": "O", "Л": "L", "Д": "D", "Ж": "Zh", "Э": "Je", "Я": "Ya",
    "Ч": "Ch", "С": "S", "М": "M", "И": "I", "Т": "T", "Ь": "'",
    "Б": "B", "Ю": "Ju", "Ё": "Jo"
}

def transliterate(text):
    result = []
    for char in text:
        if char in translit_table:
            result.append(translit_table[char])
        else:
            result.append(char)
    return "".join(result)

def main():
    with open("cyrillic.txt", "r", encoding="utf-8") as file:
        text = file.read()

    transliterated_text = transliterate(text)

    with open("transliteration.txt", "w", encoding="utf-8") as file:
        file.write(transliterated_text)

if __name__ == "__main__":
    main()