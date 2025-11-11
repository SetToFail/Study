import re

class MinimalCalculator:
    """Минимальный калькулятор с базовой функциональностью"""

    def calculate(self, expression):
        expr = expression.replace(' ', '')

        if not re.match(r'^[0-9+\-*/().]+$', expr):
            raise ValueError("Недопустимые символы в выражении")

        if expr.count('(') != expr.count(')'):
            raise ValueError("Несоответствие скобок")

        try:
            result = eval(expr)
            return result
        except ZeroDivisionError:
            raise ValueError("Деление на ноль")
        except:
            raise ValueError("Некорректное выражение")

    def interactive_calculator(self):
        print("=== ПРОСТОЙ КАЛЬКУЛЯТОР ===")
        print("Поддерживаемые операции: + - * / и скобки ()")
        print("Для выхода введите 'exit' или 'quit'")
        print("-" * 40)

        while True:
            try:
                user_input = input("Введите выражение: ").strip()

                if user_input.lower() in ['exit', 'quit', 'выход']:
                    print("До свидания!")
                    break

                if not user_input:
                    continue

                result = self.calculate(user_input)
                print(f"Результат: {result}")

            except ValueError as e:
                print(f"Ошибка: {e}")
            except KeyboardInterrupt:
                print("\nПрограмма прервана пользователем")
                break
            except Exception as e:
                print(f"Неизвестная ошибка: {e}")

if __name__ == "__main__":
    calc = MinimalCalculator()
    calc.interactive_calculator()