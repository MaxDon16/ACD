def quick_sort(arr):
    """
    Реализация алгоритма Быстрой Сортировки.

    :param arr: Список чисел для сортировки.
    :return: Отсортированный список.
    """
    # 1. Базовый случай: Если список содержит 0 или 1 элемент, он уже отсортирован.
    if len(arr) <= 1:
        return arr

    # 2. Выбор опорного элемента (pivot):
    # В данном случае, выбираем средний элемент для простоты,
    # но можно выбирать первый, последний или случайный.
    pivot_index = len(arr) // 2
    pivot = arr[pivot_index]

    # 3. Разделение: Создаем три подсписка:
    # - Элементы меньше опорного
    # - Элементы равные опорному (для обработки дубликатов)
    # - Элементы больше опорного
    less = []
    equal = []
    greater = []

    for x in arr:
        if x < pivot:
            less.append(x)
        elif x == pivot:
            equal.append(x)
        else:
            greater.append(x)

    # 4. Рекурсивный вызов: Рекурсивно сортируем подсписки 'less' и 'greater',
    # а затем объединяем их с 'equal' в правильном порядке.
    return quick_sort(less) + equal + quick_sort(greater)


# --- Пример использования ---
sequence = [10, 7, 8, 9, 1, 5]
print(f"Исходная последовательность: {sequence}")

sorted_sequence = quick_sort(sequence)
print(f"Отсортированная последовательность: {sorted_sequence}")

# --- Дополнительный пример с дубликатами ---
sequence_with_duplicates = [3, 1, 4, 1, 5, 9, 2, 6, 5]
sorted_sequence_duplicates = quick_sort(sequence_with_duplicates)
print(f"Отсортированная последовательность с дубликатами: {sorted_sequence_duplicates}")

#O(n log n) сложность 
