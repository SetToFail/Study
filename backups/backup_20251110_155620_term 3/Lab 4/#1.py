import random
import string

def generate_password(length=12, use_digits=True, use_special_chars=True):
    
    characters = string.ascii_letters
    
    if use_digits:
        characters += string.digits
    
    if use_special_chars:
        characters += "!@#$%^&*()_+-=[]{}|;:,.<>?"
    
    password = ''.join(random.choice(characters) for _ in range(length))
    
    return password

def main():
    print("=== Генератор паролей ===")
    
    try:
        length = int(input("Длина пароля (по умолчанию 12): ") or 12)
        use_digits = input("Использовать цифры? (y/n, по умолчанию y): ").lower() != 'n'
        use_special = input("Использовать спецсимволы? (y/n, по умолчанию y): ").lower() != 'n'
        
        password = generate_password(length, use_digits, use_special)
        
        print(f"\nСгенерированный пароль: {password}")
        print(f"Длина: {len(password)} символов")
        
    except ValueError:
        print("Ошибка: введите корректное число для длины пароля")

if __name__ == "__main__":
    main()