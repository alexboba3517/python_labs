"""ЛР6: текстовые CLI-утилиты — подкоманды cat и stats.

cat   — выводит файл построчно, с флагом -n нумерует строки.
stats — считает слова в тексте функциями из ЛР3 (src/lib/text.py)
        и печатает топ самых частых.

Ошибки аргументов обрабатывает argparse (код выхода 2), ошибки
чтения файла перехватываются в main() (код выхода 1).

Запуск из корня репозитория:
    python -m src.lab06.cli_text cat --input data/samples/people.csv -n
    python -m src.lab06.cli_text stats --input data/lab03/sample.txt --top 5
"""

import argparse
import sys
from pathlib import Path

from src.lib.text import count_freq, normalize, tokenize, top_n


def cat(path: Path, number: bool) -> None:
    """Печатает файл построчно.

    Файл читается лениво, по одной строке, поэтому размер файла
    не ограничен памятью.

    Args:
        path: путь к текстовому файлу в UTF-8.
        number: если True — перед каждой строкой печатается её номер.

    Raises:
        FileNotFoundError: файла нет.
        UnicodeDecodeError: файл не является текстом в UTF-8.
        OSError: файл нельзя открыть (например, это папка).
    """
    with path.open(encoding="utf-8") as f:
        for i, line in enumerate(f, start=1):
            line = line.rstrip("\n")
            if number:
                print(f"{i:>4}  {line}")
            else:
                print(line)


def stats(path: Path, top: int) -> None:
    """Печатает число слов, число уникальных слов и топ самых частых.

    Текст проходит конвейер из ЛР3: normalize -> tokenize ->
    count_freq -> top_n.

    Args:
        path: путь к текстовому файлу в UTF-8.
        top: сколько самых частых слов вывести (положительное число).

    Raises:
        FileNotFoundError: файла нет.
        UnicodeDecodeError: файл не является текстом в UTF-8.
        OSError: файл нельзя открыть (например, это папка).
    """
    text = path.read_text(encoding="utf-8")
    words = tokenize(normalize(text))
    freq = count_freq(words)

    print(f"Всего слов: {len(words)}")
    print(f"Уникальных слов: {len(freq)}")
    print(f"Топ-{top}:")
    for word, count in top_n(freq, top):
        print(f"{word}:{count}")


def main() -> None:
    """Разбирает аргументы командной строки и запускает подкоманду.

    Коды выхода: 0 — успех, 1 — ошибка при чтении файла,
    2 — неверные аргументы (выставляет argparse).
    """
    parser = argparse.ArgumentParser(description="Текстовые утилиты (ЛР6)")
    subparsers = parser.add_subparsers(dest="command", required=True)

    cat_parser = subparsers.add_parser("cat", help="вывести содержимое файла")
    cat_parser.add_argument("--input", required=True, help="путь к файлу")
    cat_parser.add_argument("-n", action="store_true", help="нумеровать строки")

    stats_parser = subparsers.add_parser("stats", help="частоты слов в тексте")
    stats_parser.add_argument("--input", required=True, help="путь к .txt")
    stats_parser.add_argument(
        "--top", type=int, default=5, help="сколько слов вывести (по умолчанию 5)"
    )

    args = parser.parse_args()

    if args.command == "stats" and args.top < 1:
        parser.error("--top должен быть положительным числом")

    path = Path(args.input)
    try:
        if args.command == "cat":
            cat(path, args.n)
        elif args.command == "stats":
            stats(path, args.top)
    except FileNotFoundError:
        print(f"Ошибка: файл не найден: {args.input}", file=sys.stderr)
        sys.exit(1)
    except UnicodeDecodeError:
        print(
            f"Ошибка: файл не является текстом в UTF-8: {args.input}",
            file=sys.stderr,
        )
        sys.exit(1)
    except OSError as e:
        print(
            f"Ошибка: не удалось прочитать {args.input}: {e.strerror}",
            file=sys.stderr,
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
