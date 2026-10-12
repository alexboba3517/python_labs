"""ЛР3, задание B: статистика слов по тексту из stdin.

Читает весь ввод до EOF (sys.stdin.read()), прогоняет его через
normalize -> tokenize -> count_freq -> top_n из lib/text.py и печатает
общее число слов, число уникальных слов и топ-5 по частоте.

Топ можно вывести списком (по умолчанию) или выровненной таблицей.
Табличный режим включается переменной окружения TEXT_STATS_TABLE=1.

Запуск из корня репозитория:
    echo "Привет, мир! Привет!!!" | python src/lab03/text_stats.py
"""

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lib.text import count_freq, normalize, tokenize, top_n  # noqa: E402

TOP_COUNT = 5
TABLE_ENV_VAR = "TEXT_STATS_TABLE"
WORD_HEADER = "слово"
COUNT_HEADER = "частота"
COLUMN_SEPARATOR = " | "


def is_table_mode() -> bool:
    """Проверяет, включён ли табличный режим через переменную окружения."""
    return os.environ.get(TABLE_ENV_VAR, "0") == "1"


def print_list(ranked: list[tuple[str, int]]) -> None:
    """Печатает топ построчно в формате «слово:кол-во»."""
    for word, count in ranked:
        print(f"{word}:{count}")


def print_table(ranked: list[tuple[str, int]]) -> None:
    """Печатает топ таблицей с выровненным столбцом слов.

    Ширина столбца «слово» равна длине самого длинного слова в топе,
    но не меньше длины заголовка.
    """
    width = max([len(WORD_HEADER)] + [len(word) for word, _ in ranked])
    header = f"{WORD_HEADER:<{width}}{COLUMN_SEPARATOR}{COUNT_HEADER}"
    print(header)
    print("-" * len(header))
    for word, count in ranked:
        print(f"{word:<{width}}{COLUMN_SEPARATOR}{count}")


def main() -> None:
    """Читает текст из stdin и печатает статистику слов."""
    sys.stdin.reconfigure(encoding="utf-8")
    text = sys.stdin.read()

    normalized = normalize(text)
    words = tokenize(normalized)
    frequencies = count_freq(words)
    ranked = top_n(frequencies, TOP_COUNT)

    print(f"Всего слов: {len(words)}")
    print(f"Уникальных слов: {len(frequencies)}")
    print(f"Топ-{TOP_COUNT}:")
    if is_table_mode():
        print_table(ranked)
    else:
        print_list(ranked)


if __name__ == "__main__":
    main()
