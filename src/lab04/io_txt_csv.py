"""Ввод/вывод для лабораторных: чтение текстовых файлов и запись CSV.

Модуль создан в ЛР4 (задание A) и переиспользуется в следующих
лабораторных. Функции ничего не считают и не печатают — только читают
и пишут файлы. Ошибки чтения не перехватываются, а передаются
вызывающему коду.
"""

import csv
from pathlib import Path


def read_text(path: str | Path, encoding: str = "utf-8") -> str:
    """Читает текстовый файл целиком и возвращает его содержимое одной строкой.

    Файл читается сразу полностью — для учебных файлов в пару килобайт
    это проще всего. Для очень больших файлов лучше читать построчно
    (for line in f), чтобы не держать весь текст в памяти.

    Args:
        path: путь к файлу — строка или Path. Относительный путь
            считается от папки, из которой запущен Python.
        encoding: кодировка файла, по умолчанию "utf-8". Если файл
            сохранён в другой кодировке (например, в Блокноте Windows
            как ANSI), передайте её явно: read_text(path, encoding="cp1251").

    Returns:
        Содержимое файла. Для пустого файла — пустая строка "".

    Raises:
        FileNotFoundError: если файла по такому пути нет.
        UnicodeDecodeError: если байты файла не читаются в указанной
            кодировке (файл в cp1251, а читаем как utf-8).
        LookupError: если кодировки с таким названием не существует.
    """
    p = Path(path)
    with p.open("r", encoding=encoding) as f:
        return f.read()


def write_csv(
    rows: list[tuple | list],
    path: str | Path,
    header: tuple[str, ...] | None = None,
) -> None:
    """Записывает строки в CSV-файл с разделителем ",".

    Если файл уже существует, он перезаписывается. Недостающие папки
    создаются. Файл пишется в кодировке UTF-8. Длина строк проверяется
    до открытия файла, поэтому при ошибке старый файл остаётся нетронутым.

    Args:
        rows: список строк таблицы; каждая строка — кортеж или список
            значений, например [("привет", 2), ("мир", 1)].
        path: путь к CSV-файлу — строка или Path.
        header: заголовок — кортеж названий колонок, например
            ("word", "count"). Если передан, записывается первой строкой.
            Если None — файл без заголовка.

    Raises:
        ValueError: если строки в rows разной длины или их длина
            не совпадает с длиной header.
    """
    rows = list(rows)

    if header is not None:
        expected_len = len(header)
    elif rows:
        expected_len = len(rows[0])
    else:
        expected_len = 0

    for i, row in enumerate(rows, start=1):
        if len(row) != expected_len:
            raise ValueError(
                f"write_csv: строка {i} содержит {len(row)} значений, "
                f"ожидалось {expected_len}"
            )

    p = Path(path)
    ensure_parent_dir(p)

    with p.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        if header is not None:
            writer.writerow(header)
        writer.writerows(rows)


def ensure_parent_dir(path: str | Path) -> None:
    """Создаёт папку, в которой будет лежать файл, если её ещё нет.

    Создаётся вся цепочка недостающих папок: для "data/out/report.csv"
    будут созданы и data, и data/out. Если папка уже существует,
    ничего не происходит.

    Args:
        path: путь к ФАЙЛУ (не к папке) — строка или Path.
    """
    Path(path).parent.mkdir(parents=True, exist_ok=True)
