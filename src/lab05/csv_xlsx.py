"""Конвертация CSV -> XLSX (ЛР5, задание B).

Единственная сторонняя зависимость лабораторной - openpyxl
(pip install -r requirements.txt).
"""

import csv
from pathlib import Path

from openpyxl import Workbook


def csv_to_xlsx(csv_path: str, xlsx_path: str) -> None:
    """Конвертирует CSV в XLSX-файл с одним листом "Sheet1".

    Первая строка CSV (заголовок) переносится как обычная первая строка
    листа. Ширина каждой колонки - длина самого длинного значения в ней,
    но не меньше 8 символов. Значения переносятся как текст, типы
    не преобразуются. Папка для выходного файла создаётся, если её нет.

    Args:
        csv_path: путь к входному .csv, относительно текущей папки.
        xlsx_path: путь к выходному .xlsx. Существующий файл перезаписывается.

    Raises:
        FileNotFoundError: входного файла нет.
        ValueError: расширение не .csv или CSV пустой.
    """
    csv_file = Path(csv_path)

    if not csv_file.exists():
        raise FileNotFoundError(f"Файл не найден: {csv_path}")
    if csv_file.suffix != ".csv":
        raise ValueError(f"Ожидался файл .csv, получен: {csv_file.suffix}")

    with csv_file.open(encoding="utf-8", newline="") as f:
        rows = list(csv.reader(f))

    if not rows:
        raise ValueError("CSV пустой")

    wb = Workbook()
    ws = wb.active
    ws.title = "Sheet1"

    for row in rows:
        ws.append(row)

    for column in ws.columns:
        max_len = max(len(str(cell.value or "")) for cell in column)
        letter = column[0].column_letter
        ws.column_dimensions[letter].width = max(max_len, 8)

    xlsx_file = Path(xlsx_path)
    xlsx_file.parent.mkdir(parents=True, exist_ok=True)
    wb.save(xlsx_file)


if __name__ == "__main__":
    csv_to_xlsx("data/samples/people.csv", "data/out/people.xlsx")
