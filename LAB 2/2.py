"""
Лаба №2 "Задача об арифметическом выражении"

На вход подаётся математическое выражение. Элементы - числа. Операции - "+ - * /". Также есть скобочки. Окончанием выражения служит "=". Программа должна вывести результат выражения

Пример ввода:
2+7*(3/9)-5=

Замечание:
Программа также должна делать "проверку на дурака": нет деления на 0, все скобки стоят верно (см лабу №1) и т.п.
"""
from queue import LifoQueue

#словарь открыв и закрыв
BRACKETS_INFO = {
    ")":  "(",
    "]":  "[",
    "}":  "{"
}

PRIORITY = {
    "start": 0,
    "(": 1,
    ")": 1,
    "+": 2,
    "-": 2,
    "*": 3,
    "/": 3,
}

"""
string - строка где ошибка
position - позиция ошибки в строке
print_correctness - нужно ли печатать "Строка не существует!"
text - текст ошибки (по умолчанию "Incorrect bracket!")
"""
def printing_errors(string: str, position: int, print_correctness: bool, text="Incorrect bracket!") -> None:
    if print_correctness:
        print("Строка не существует!")
    print("Ошибка ")
    print(string)
    print("^".rjust(position + 1))
    print(text)

def check_brackets(brackets: str, BRACKETS_INFO: dict, print_correctness=True, print_errors=True, accept_num=False, accept_alpha=False) -> bool:
    lifo = LifoQueue() #Создаем стек (LIFO - Last In First Out)
    for position, bracket in enumerate(brackets):
        if bracket in BRACKETS_INFO.values():
            lifo.put(bracket)
        elif bracket in BRACKETS_INFO.keys():
            if lifo.empty() or (BRACKETS_INFO[bracket] != lifo.get()):
                if print_errors:
                    printing_errors(brackets, position, print_correctness)
                return False
        else:
            if (not accept_num) and (bracket in "0123456789+-/*."):
                if print_errors:
                    printing_errors(brackets, position, print_correctness,
                                  text="Incorrect symbol! Expected bracket, number or arithmetical operation.")
                return False
            if (not accept_alpha) and (bracket.isalpha()):
                if print_errors:
                    printing_errors(brackets, position, print_correctness,
                                  text="Incorrect symbol! Expected bracket or alpha.")
                return False
    else:
        if lifo.empty():
            if print_correctness:
                print("Строка существует")
            return True
        else:
            if print_errors:
                printing_errors(brackets, brackets.rfind(lifo.get()), print_correctness,
                              text="The bracket was never closed!")
            return False


def tokenize(expression: str) -> list[str]:
    """Разбивает выражение на токены"""
    expression = expression.replace(" ", "")

    # Проверяем, что выражение заканчивается на =
    if not expression.endswith("="):
        raise SyntaxError("Expression must end with '='")

    expression = expression.removesuffix("=")

    # Проверяем скобки и допустимые символы
    if not check_brackets(expression, {")": "("}, print_correctness=False, print_errors=False, accept_num=True):
        raise SyntaxError("Invalid brackets or symbols in expression")

    # Добавляем пробелы вокруг операторов для разделения
    for sym in "+-*/()":
        expression = expression.replace(sym, f" {sym} ")

    # Убираем лишние пробелы и возвращаем список токенов
    tokens = [token for token in expression.split() if token] #1
    return tokens
"""
Объяснение 1 : Это называется list comprehension (генератор списка). Разберем:
expression.split() - разбивает строку по пробелам на список
for token in expression.split() - для каждого элемента в этом списке
if token - если элемент не пустой строкой
[token ...] - добавляем его в новый список
"""

def convert_to_rpn(tokens: list[str]) -> list[str]:
    """Конвертирует инфиксную запись в обратную польскую запись (RPN)"""
    result = []
    stack = ["start"]  # Стек операторов

    for token in tokens:
        if token.isnumeric() or (token[0] == '-' and token[1:].isnumeric() and not stack): # Число (включая отрицательные числа в начале выражения)
            result.append(token)

        elif token == "(":  # Открывающая скобка - в стек
            stack.append(token)

        elif token == ")":  # Закрывающая скобка - выталкиваем до открывающей
            while stack and stack[-1] != "(":
                if stack[-1] == "start":
                    raise SyntaxError("Mismatched brackets")
                result.append(stack.pop())

            if not stack or stack[-1] != "(":
                raise SyntaxError("Mismatched brackets")
            stack.pop()  # Убираем "("

        elif token in "+-*/":
            # Обработка унарного минуса
            if token == "-" and (not result or (stack and stack[-1] == "(")):
                result.append("0")
                stack.append("-")
                continue

            # Обработка бинарных операторов
            while (stack and stack[-1] != "start" and stack[-1] != "(" and
                   PRIORITY[stack[-1]] >= PRIORITY[token]):
                result.append(stack.pop())

            stack.append(token)

    # Выталкиваем оставшиеся операторы из стека
    while stack and stack[-1] != "start":
        if stack[-1] == "(":
            raise SyntaxError("Mismatched brackets")
        result.append(stack.pop())

    return result


def evaluate_rpn(tokens: list[str]) -> float:
    """Вычисляет выражение в обратной польской записи"""
    stack = LifoQueue()

    for token in tokens:
        if token not in "+-*/":
            # Число
            stack.put(float(token))
        else:
            # Оператор - извлекаем два операнда
            if stack.qsize() < 2:
                raise SyntaxError("Invalid expression: not enough operands")

            right = stack.get()
            left = stack.get()

            match token:
                case '+':
                    stack.put(left + right)
                case '-':
                    stack.put(left - right)
                case '*':
                    stack.put(left * right)
                case '/':
                    if right == 0:
                        raise ZeroDivisionError("Division by zero")
                    stack.put(left / right)

    if stack.qsize() != 1:
        raise SyntaxError("Invalid expression")

    return stack.get()


def calculate_expression(expression: str) -> float:
    """Основная функция для вычисления выражения"""
    try:
        # Шаг 1: Разбиваем на токены
        tokens = tokenize(expression)
        print(f"Токены: {tokens}")

        # Шаг 2: Конвертируем в RPN
        rpn_tokens = convert_to_rpn(tokens)
        print(f"RPN: {rpn_tokens}")

        # Шаг 3: Вычисляем
        result = evaluate_rpn(rpn_tokens)

        return result

    except Exception:
        # Общая обработка всех ошибок
        raise


def main():
    """Основная функция программы"""

    while True:
        try:
            expression = input("\nВведите выражение").strip()


            if not expression:
                continue

            result = calculate_expression(expression)

            # Красивый вывод результата
            if result.is_integer():
                print(f"Результат: {int(result)}")
            else:
                print(f"Результат: {result:.6f}")

        except Exception:
            print("Ошибка! Проверьте правильность выражения.")
            print("Убедитесь, что:")
            print("- Выражение заканчивается на '='")
            print("- Скобки расставлены правильно")
            print("- Нет деления на ноль")
            print("- Используются только числа и операторы + - * /")


if __name__ == "__main__":
    # Запуск основной программы
    main()
