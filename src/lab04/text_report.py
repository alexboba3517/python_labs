"""Отчёт о частотах слов в текстовых файлах с выгрузкой в CSV.

Скрипт создан в ЛР4 (задание B и ★). Читает текст из файла, прогоняет
его через normalize → tokenize → count_freq из lib/text.py, сохраняет
частоты всех слов в CSV (count по убыванию, при равенстве — слово
по алфавиту) и печатает краткое резюме в консоль.

Режимы:
    * один входной файл — отчёт word,count;
    * несколько файлов (★) — отчёт file,word,count по каждому файлу
      и сводный отчёт word,count по всем файлам вместе.

Запуск — из корня репозитория, как модуль:
    python -m src.lab04.text_report
    python -m src.lab04.text_report --in data/lab04/input.txt --out data/lab04/report.csv
    python -m src.lab04.text_report --in data/lab04/a.txt data/lab04/b.txt --table
"""

import argparse
import sys
from pathlib import Path

from src.lab04.io_txt_csv import read_text, write_csv
from src.lib.text import count_freq, normalize, tokenize, top_n

TOP_COUNT = 3
REPORT_HEADER = ("word", "count")
PER_FILE_HEADER = ("file", "word", "count")
DEFAULT_INPUT = "data/lab04/input.txt"
DEFAULT_OUTPUT = "data/lab04/report.csv"
DEFAULT_PER_FILE = "data/lab04/report_per_file.csv"
DEFAULT_TOTAL = "data/lab04/report_total.csv"
DEFAULT_ENCODING = "utf-8"


def count_words(text: str) -> dict[str, int]:
    """Считает частоты слов в тексте.

    Текст нормализуется и разбивается на слова функциями из lib/text.py.

    Args:
        text: исходный текст.

    Returns:
        Словарь «слово → количество». Для пустого текста — {}.

    Examples:
        >>> count_words("Привет, мир! Привет!!!")
        {'привет': 2, 'мир': 1}
        >>> count_words("")
        {}
    """
    return count_freq(tokenize(normalize(text)))


def sorted_word_counts(freq: dict[str, int]) -> list[tuple[str, int]]:
    """Возвращает все пары (слово, частота), отсортированные для отчёта.

    Порядок: частота по убыванию, при равной частоте — слово по алфавиту.
    Это тот же порядок, что у top_n, только без ограничения по количеству.

    Args:
        freq: словарь «слово → количество».

    Returns:
        Список пар (слово, частота). Для пустого словаря — [].

    Examples:
        >>> sorted_word_counts({"b": 1, "a": 1, "c": 3})
        [('c', 3), ('a', 1), ('b', 1)]
        >>> sorted_word_counts({})
        []
    """
    return top_n(freq, len(freq))


def merge_freqs(freqs: list[dict[str, int]]) -> dict[str, int]:
    """Складывает несколько словарей частот в один сводный.

    Если слово есть в нескольких словарях, его частоты суммируются.
    Входные словари не изменяются.

    Args:
        freqs: список словарей «слово → количество».

    Returns:
        Сводный словарь «слово → количество». Для пустого списка — {}.

    Examples:
        >>> merge_freqs([{"привет": 1, "мир": 1}, {"привет": 2}])
        {'привет': 3, 'мир': 1}
        >>> merge_freqs([])
        {}
    """
    total: dict[str, int] = {}
    for freq in freqs:
        for word, count in freq.items():
            total[word] = total.get(word, 0) + count
    return total


def per_file_rows(
    freqs_by_file: dict[str, dict[str, int]],
) -> list[tuple[str, str, int]]:
    """Готовит строки отчёта по каждому файлу: (файл, слово, частота).

    Порядок: имя файла по алфавиту, внутри файла — частота по убыванию,
    при равной частоте — слово по алфавиту.

    Args:
        freqs_by_file: словарь «имя файла → словарь частот этого файла».

    Returns:
        Список строк (файл, слово, частота).

    Examples:
        >>> per_file_rows({"b.txt": {"привет": 2}, "a.txt": {"привет": 1, "мир": 1}})
        [('a.txt', 'мир', 1), ('a.txt', 'привет', 1), ('b.txt', 'привет', 2)]
    """
    rows = []
    for file_name, freq in freqs_by_file.items():
        for word, count in freq.items():
            rows.append((file_name, word, count))
    rows.sort(key=lambda row: (row[0], -row[2], row[1]))
    return rows


def print_summary(freq: dict[str, int]) -> None:
    """Печатает число всех слов, число уникальных слов и топ-5 самых частых.

    Args:
        freq: словарь «слово → количество».
    """
    print(f"Всего слов: {sum(freq.values())}")
    print(f"Уникальных слов: {len(freq)}")
    print(f"Топ-{TOP_COUNT}:")
    for word, count in top_n(freq, TOP_COUNT):
        print(f"{word}:{count}")


def print_table(header: tuple[str, ...], rows: list[tuple]) -> None:
    """Печатает строки таблицей с выровненными столбцами.

    Ширина каждого столбца — по самому длинному значению в нём
    (включая заголовок). Работает с любым числом столбцов.

    Args:
        header: названия столбцов, например ("word", "count").
        rows: строки таблицы той же длины, что header.
    """
    widths = [len(h) for h in header]
    for row in rows:
        for i, value in enumerate(row):
            widths[i] = max(widths[i], len(str(value)))

    print(" | ".join(f"{h:<{w}}" for h, w in zip(header, widths)))
    print("-+-".join("-" * w for w in widths))
    for row in rows:
        print(" | ".join(f"{str(v):<{w}}" for v, w in zip(row, widths)))


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Разбирает аргументы командной строки.

    Один входной файл — базовый режим: отчёт в --out.
    Несколько файлов (или указан --per-file / --total) — режим ★:
    отчёт по каждому файлу и сводный отчёт.

    Args:
        argv: список аргументов; None — взять из sys.argv.

    Returns:
        Объект с полями inputs, output, per_file, total, encoding, table.
    """
    parser = argparse.ArgumentParser(
        description="Считает частоты слов в текстовых файлах и сохраняет их в CSV.",
    )
    parser.add_argument(
        "--in",
        dest="inputs",
        nargs="+",
        default=[DEFAULT_INPUT],
        help=f"один или несколько входных файлов (по умолчанию {DEFAULT_INPUT})",
    )
    parser.add_argument(
        "--out",
        dest="output",
        default=DEFAULT_OUTPUT,
        help=f"отчёт для одного файла (по умолчанию {DEFAULT_OUTPUT})",
    )
    parser.add_argument(
        "--per-file",
        dest="per_file",
        default=None,
        help=f"★ отчёт по каждому файлу (по умолчанию {DEFAULT_PER_FILE})",
    )
    parser.add_argument(
        "--total",
        default=None,
        help=f"★ сводный отчёт по всем файлам (по умолчанию {DEFAULT_TOTAL})",
    )
    parser.add_argument(
        "--encoding",
        default=DEFAULT_ENCODING,
        help=f"кодировка входных файлов (по умолчанию {DEFAULT_ENCODING})",
    )
    parser.add_argument(
        "--table",
        action="store_true",
        help="дополнительно напечатать отчёт таблицей",
    )
    return parser.parse_args(argv)


def load_text(path: str, encoding: str) -> str:
    """Читает файл для отчёта; при ошибке сообщает в stderr и выходит с кодом 1.

    Обёртка над read_text для консольной программы: превращает
    исключения в понятные сообщения пользователю. Обрабатываются:
    файл не найден, путь — папка или нет прав (OSError), неверная
    кодировка файла (UnicodeDecodeError), неизвестное название
    кодировки (LookupError).

    Args:
        path: путь к входному файлу.
        encoding: кодировка файла.

    Returns:
        Содержимое файла.
    """
    try:
        return read_text(path, encoding=encoding)
    except FileNotFoundError:
        print(f"Ошибка: файл не найден: {path}", file=sys.stderr)
        sys.exit(1)
    except OSError as e:
        print(f"Ошибка: не удалось открыть {path}: {e.strerror}", file=sys.stderr)
        sys.exit(1)
    except UnicodeDecodeError:
        print(
            f"Ошибка: не удалось прочитать {path} в кодировке "
            f"{encoding}. Проверьте кодировку файла, например: "
            "--encoding cp1251",
            file=sys.stderr,
        )
        sys.exit(1)
    except LookupError:
        print(f"Ошибка: неизвестная кодировка: {encoding}", file=sys.stderr)
        sys.exit(1)


def run_single(path: str, output: str, encoding: str, table: bool) -> None:
    """Базовый режим: один файл → один отчёт word,count.

    Args:
        path: входной текстовый файл.
        output: путь к CSV-отчёту.
        encoding: кодировка входного файла.
        table: печатать ли отчёт таблицей после резюме.
    """
    freq = count_words(load_text(path, encoding))
    rows = sorted_word_counts(freq)
    write_csv(rows, output, header=REPORT_HEADER)
    print_summary(freq)
    if table:
        print()
        print_table(REPORT_HEADER, rows)


def run_many(
    paths: list[str],
    per_file_path: str,
    total_path: str,
    encoding: str,
    table: bool,
) -> None:
    """Режим ★: несколько файлов → отчёт по каждому и сводный отчёт.

    Сначала читаются все файлы, затем пишутся отчёты: если какой-то
    файл не прочитался, ни один отчёт не перезаписывается.

    Args:
        paths: входные текстовые файлы.
        per_file_path: путь к отчёту file,word,count.
        total_path: путь к сводному отчёту word,count.
        encoding: кодировка входных файлов.
        table: печатать ли отчёт по файлам таблицей после резюме.
    """
    freqs_by_file: dict[str, dict[str, int]] = {}
    for path in paths:
        name = Path(path).name
        if name in freqs_by_file:
            print(
                f"Ошибка: два входных файла с одинаковым именем {name}",
                file=sys.stderr,
            )
            sys.exit(1)
        freqs_by_file[name] = count_words(load_text(path, encoding))

    total = merge_freqs(list(freqs_by_file.values()))
    file_rows = per_file_rows(freqs_by_file)

    write_csv(file_rows, per_file_path, header=PER_FILE_HEADER)
    write_csv(sorted_word_counts(total), total_path, header=REPORT_HEADER)

    print(f"Файлов: {len(freqs_by_file)}")
    print_summary(total)
    if table:
        print()
        print_table(PER_FILE_HEADER, file_rows)


def main(argv: list[str] | None = None) -> None:
    """Точка входа: выбирает режим по аргументам и запускает его.

    Args:
        argv: список аргументов; None — взять из sys.argv.
    """
    args = parse_args(argv)
    many = (
        len(args.inputs) > 1
        or args.per_file is not None
        or args.total is not None
    )
    if many:
        run_many(
            args.inputs,
            args.per_file or DEFAULT_PER_FILE,
            args.total or DEFAULT_TOTAL,
            args.encoding,
            args.table,
        )
    else:
        run_single(args.inputs[0], args.output, args.encoding, args.table)


if __name__ == "__main__":
    main()
