import os
"Внешняя Многофазная Сортировка (External Polyphase Merge Sort)"
# ------- ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ -------

def read_numbers(filename):
    with open(filename, "r") as f:
        return list(map(int, f.read().split()))

def write_numbers(filename, numbers):
    with open(filename, "w") as f:
        f.write(" ".join(map(str, numbers)))

def merge(list1, list2):
    """Слияние двух отсортированных списков."""
    result = []
    i = j = 0

    while i < len(list1) and j < len(list2):
        if list1[i] <= list2[j]:
            result.append(list1[i])
            i += 1
        else:
            result.append(list2[j])
            j += 1

    result.extend(list1[i:])
    result.extend(list2[j:])
    return result


# ------- ГЕНЕРАЦИЯ СЕРИЙ -------

def create_runs(input_file, run_size=5):
    """Разбиваем исходный файл на отсортированные серии."""
    numbers = read_numbers(input_file)

    runs = []
    for i in range(0, len(numbers), run_size):
        run = numbers[i:i + run_size]
        run.sort()
        runs.append(run)

    return runs


# ------- РАСПРЕДЕЛЕНИЕ ПО ФАЙЛАМ -------

def distribute_runs(runs, f1, f2):
    """Распределяем серии по 2 файлам."""
    # упрощённая версия метода Фибоначчи
    toggle = True
    for run in runs:
        if toggle:
            write_numbers(f1, run)
        else:
            write_numbers(f2, run)
        toggle = not toggle


# ------- СЛИЯНИЕ ФАЗАМИ -------

def polyphase_merge(f1, f2, out):
    """Простая модель многофазного слияния."""
    "В реальной многофазной сортировке файлов 3 и более"
    a = read_numbers(f1)
    b = read_numbers(f2)

    result = merge(a, b)
    write_numbers(out, result)


# ------- ОСНОВНАЯ ПРОГРАММА -------

def external_polyphase_sort(input_file, output_file):
    # 1. Создаём отсортированные серии
    runs = create_runs(input_file)

    # 2. Распределяем серии по двум файлам
    distribute_runs(runs, "f1.txt", "f2.txt")

    # 3. Выполняем многофазное слияние
    polyphase_merge("f1.txt", "f2.txt", output_file)


# ------- ЗАПУСК -------

# Создаём пример входного файла
write_numbers("input.txt", [8, 3, 5, 1, 9, 2, 7, 6])

external_polyphase_sort("input.txt", "sorted.txt")

print("Отсортированный файл:", read_numbers("sorted.txt"))
