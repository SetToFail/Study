import os
from pathlib import Path

class InteractiveRenamer:
    def __init__(self):
        self.current_directory = None
        self.files = []
    
    def clear_screen(self):
        """Очистка экрана"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def show_header(self):
        """Показ заголовка"""
        print("=" * 50)
        print("       МАССОВОЕ ПЕРЕИМЕНОВАНИЕ ФАЙЛОВ")
        print("=" * 50)
        
        if self.current_directory:
            print(f"Текущая папка: {self.current_directory}")
            print(f"Файлов: {len(self.files)}")
        print()
    
    def select_directory(self):
        """Выбор директории"""
        self.clear_screen()
        self.show_header()
        
        directory = input("Введите путь к папке: ") 
        
        if not directory:
            print("Используется текущая папка")
            directory = "."
        
        if not os.path.exists(directory):
            print("Ошибка: Папка не существует!")
            input("Нажмите Enter для продолжения...")
            return False
        
        self.current_directory = directory
        self.files = [f for f in Path(directory).iterdir() if f.is_file()]
        
        if not self.files:
            print("В папке нет файлов!")
            input("Нажмите Enter для продолжения...")
            return False
        
        return True
    
    def show_files_preview(self):
        """Показ превью файлов"""
        print("\nСписок файлов:")
        print("-" * 40)
        for i, file in enumerate(self.files[:10]):  
            print(f"{i+1:2d}. {file.name}")
        if len(self.files) > 10:
            print(f"... и еще {len(self.files) - 10} файлов")
        print("-" * 40)
    
    def show_menu(self):
        """Главное меню"""
        self.clear_screen()
        self.show_header()
        
        if not self.current_directory:
            print("Сначала выберите папку с файлами")
            return "select_directory"
        
        self.show_files_preview()
        
        print("\nВЫБЕРИТЕ ДЕЙСТВИЕ:")
        print("1. Последовательная нумерация")
        print("2. Добавить префикс")
        print("3. Добавить суффикс") 
        print("4. Заменить текст")
        print("5. Изменить регистр")
        print("6. Выбрать другую папку")
        print("0. Выход")
        
        choice = input("\nВаш выбор (0-6): ") 
        return choice
    
    def run(self):
        """Запуск интерактивного режима"""
        if not self.select_directory():
            return
            
        while True:
            choice = self.show_menu()
            
            if choice == '0':
                print("Выход из программы...")
                break
            elif choice == '1':
                self.sequential_rename()
            elif choice == '2':
                self.prefix_rename()
            elif choice == '3':
                self.suffix_rename()
            elif choice == '4':
                self.replace_rename()
            elif choice == '5':
                self.case_rename()
            elif choice == '6':
                self.select_directory()
            elif choice == 'select_directory':
                self.select_directory()
            else:
                print("Неверный выбор!")
                input("Нажмите Enter для продолжения...")
    
    def get_rename_plan(self, template_func):
        """Получить план переименования"""
        plan = []
        for i, file_path in enumerate(self.files):
            new_name = template_func(i, file_path)
            plan.append((file_path.name, new_name))
        return plan
    
    def preview_and_execute(self, plan):
        """Показать превью и выполнить переименование"""
        print("\n--- ПРЕДВАРИТЕЛЬНЫЙ ПРОСМОТР ---")
        for old_name, new_name in plan:
            print(f"{old_name} -> {new_name}")
        
        confirm = input("\nВыполнить переименование? (y/n): ") .lower()
        if confirm != 'y':
            print("Отменено")
            input("Нажмите Enter для продолжения...")
            return
        
        success_count = 0
        print("\n--- ВЫПОЛНЕНИЕ ---")
        for old_name, new_name in plan:
            try:
                old_path = Path(self.current_directory) / old_name
                new_path = Path(self.current_directory) / new_name
                
                if new_path.exists():
                    print(f"✗ Ошибка: файл {new_name} уже существует!")
                    continue
                    
                old_path.rename(new_path)
                print(f"✓ {old_name} -> {new_name}")
                success_count += 1
            except Exception as e:
                print(f"✗ Ошибка при переименовании {old_name}: {e}")
        
        print(f"\n--- РЕЗУЛЬТАТ ---")
        print(f"Успешно переименовано: {success_count} из {len(plan)} файлов")
        input("Нажмите Enter для продолжения...")
        
        self.files = [f for f in Path(self.current_directory).iterdir() if f.is_file()]
    
    def sequential_rename(self):
        """Последовательная нумерация"""
        print("\n--- ПОСЛЕДОВАТЕЛЬНАЯ НУМЕРАЦИЯ ---")
        prefix = input("Префикс (например 'photo_'): ") or 'file_'
        
        try:
            start = int(input("Начальный номер: ")  or '1')
            digits = int(input("Количество цифр: ")  or '3')
        except ValueError:
            print("Ошибка: введите корректные числа!")
            input("Нажмите Enter для продолжения...")
            return
        
        def template(i, file_path):
            return f"{prefix}{i + start:0{digits}d}{file_path.suffix}"
        
        plan = self.get_rename_plan(template)
        self.preview_and_execute(plan)
    
    def prefix_rename(self):
        """Добавление префикса"""
        print("\n--- ДОБАВЛЕНИЕ ПРЕФИКСА ---")
        prefix = input("Введите префикс: ") 
        if not prefix:
            print("Префикс не может быть пустым!")
            input("Нажмите Enter для продолжения...")
            return
        
        def template(i, file_path):
            return f"{prefix}{file_path.name}"
        
        plan = self.get_rename_plan(template)
        self.preview_and_execute(plan)
    
    def suffix_rename(self):
        """Добавление суффикса"""
        print("\n--- ДОБАВЛЕНИЕ СУФФИКСА ---")
        suffix = input("Введите суффикс: ") 
        if not suffix:
            print("Суффикс не может быть пустым!")
            input("Нажмите Enter для продолжения...")
            return
        
        def template(i, file_path):
            stem = file_path.stem
            extension = file_path.suffix
            return f"{stem}{suffix}{extension}"
        
        plan = self.get_rename_plan(template)
        self.preview_and_execute(plan)
    
    def replace_rename(self):
        """Замена текста в именах файлов"""
        print("\n--- ЗАМЕНА ТЕКСТА ---")
        old_text = input("Какой текст заменить: ") 
        if not old_text:
            print("Текст для замены не может быть пустым!")
            input("Нажмите Enter для продолжения...")
            return
            
        new_text = input("На какой текст заменить: ") 
        
        def template(i, file_path):
            return file_path.name.replace(old_text, new_text)
        
        plan = self.get_rename_plan(template)
        self.preview_and_execute(plan)
    
    def case_rename(self):
        """Изменение регистра имен файлов"""
        print("\n--- ИЗМЕНЕНИЕ РЕГИСТРА ---")
        print("1. В нижний регистр (file.txt)")
        print("2. В верхний регистр (FILE.TXT)")
        print("3. С заглавных букв (File.Txt)")
        
        choice = input("Выберите вариант (1-3): ") 
        
        def template(i, file_path):
            if choice == '1':
                return file_path.name.lower()
            elif choice == '2':
                return file_path.name.upper()
            elif choice == '3':
                return file_path.name.title()
            else:
                return file_path.name  
        
        if choice not in ['1', '2', '3']:
            print("Неверный выбор!")
            input("Нажмите Enter для продолжения...")
            return
        
        plan = self.get_rename_plan(template)
        self.preview_and_execute(plan)


if __name__ == "__main__":
    try:
        renamer = InteractiveRenamer()
        renamer.run()
    except KeyboardInterrupt:
        print("\n\nПрограмма завершена пользователем")
    except Exception as e:
        print(f"\nПроизошла непредвиденная ошибка: {e}")