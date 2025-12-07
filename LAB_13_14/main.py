import re

# -------------------------------
# Чтение слов из текстового файла
# -------------------------------
def read_words(filename):
    with open(filename, "r", encoding="utf-8") as f:
        text = f.read().lower()
    # Берём только слова: русские и английские буквы
    return re.findall(r"[a-zA-Zа-яА-ЯёЁ]+", text)


# -------------------------------
# Хеш-функция
# -------------------------------
def hash_func(s, size):
    h = 0
    for ch in s:
        h = (h * 31 + ord(ch)) % size
    return h


# ====================================================
# ЛАБА 13 — Хеш-таблица "с наложением"
# (open addressing, линейное пробирование)
# ====================================================
def build_hash_open_addressing(words, size):
    table = [None] * size

    for word in words:
        index = hash_func(word, size)

        # Линейное пробирование
        while table[index] not in (None, word):
            index = (index + 1) % size

        table[index] = word

    return table


# ====================================================
# ЛАБА 14 — Хеш-таблица со списками
# (chaining — каждый слот хранит список)
# ====================================================
def build_hash_chaining(words, size):
    table = [[] for _ in range(size)]

    for word in words:
        index = hash_func(word, size)
        if word not in table[index]:
            table[index].append(word)

    return table


# -------------------------------
# Запись таблицы в файл
# -------------------------------
def save_table(filename, title, table):
    with open(filename, "a", encoding="utf-8") as f:
        f.write("\n" + title + "\n")
        f.write("=" * len(title) + "\n")
        for i, cell in enumerate(table):
            f.write(f"{i}: {cell}\n")


# -------------------------------
# Главная программа
# -------------------------------
def main():
    input_file = "text.txt"            # входной файл
    output_file = "result.txt"         # куда записывать таблицы
    table_size = 200                   # размер хеш-таблицы

    # Очищаем результирующий файл
    open(output_file, "w").close()

    # Читаем текст и получаем слова
    words = read_words(input_file)

    # Лаба №13: метод наложения (open addressing)
    table_open = build_hash_open_addressing(words, table_size)
    save_table(output_file, "Лаба 13 — Хеш-таблица с наложением", table_open)

    # Лаба №14: таблица со списками (chaining)
    table_chain = build_hash_chaining(words, table_size)
    save_table(output_file, "Лаба 14 — Хеш-таблица со списками", table_chain)


if __name__ == "__main__":
    main()
