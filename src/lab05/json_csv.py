"""Конвертация JSON <-> CSV (ЛР5, задание A).

Функции только читают и пишут файлы: ничего не печатают, ошибки
не перехватывают, а выбрасывают вызывающему коду.
Используется только стандартная библиотека: csv, json, pathlib.
"""

import csv
import json
from pathlib import Path


def json_to_csv(json_path: str, csv_path: str) -> None:
    """Преобразует JSON-файл (список объектов) в CSV.

    Колонки - объединение ключей всех объектов: сначала ключи первого
    объекта, затем новые ключи из следующих в порядке появления.
    Отсутствующие поля заполняются пустой строкой. Папка для
    выходного файла создаётся, если её нет.

    Args:
        json_path: путь к входному .json, относительно текущей папки.
        csv_path: путь к выходному .csv. Существующий файл перезаписывается.

    Raises:
        FileNotFoundError: входного файла нет.
        ValueError: расширение не .json; JSON пустой, битый, не список
            или в списке есть не-объекты.
    """
    json_file = Path(json_path)

    if not json_file.exists():
        raise FileNotFoundError(f"Файл не найден: {json_path}")
    if json_file.suffix != ".json":
        raise ValueError(f"Ожидался файл .json, получен: {json_file.suffix}")

    with json_file.open(encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list) or not data:
        raise ValueError("Пустой JSON или неподдерживаемая структура")
    if not all(isinstance(item, dict) for item in data):
        raise ValueError("Все элементы JSON-списка должны быть объектами")

    fieldnames = []
    for item in data:
        for key in item:
            if key not in fieldnames:
                fieldnames.append(key)

    csv_file = Path(csv_path)
    csv_file.parent.mkdir(parents=True, exist_ok=True)

    with csv_file.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)


def csv_to_json(csv_path: str, json_path: str) -> None:
    """Преобразует CSV-файл с заголовком в JSON (список объектов).

    Каждая строка CSV становится объектом, ключи берутся из заголовка.
    Все значения остаются строками: в CSV нет типов. JSON пишется
    с ensure_ascii=False и indent=2. Папка для выходного файла
    создаётся, если её нет.

    Args:
        csv_path: путь к входному .csv, относительно текущей папки.
        json_path: путь к выходному .json. Существующий файл перезаписывается.

    Raises:
        FileNotFoundError: входного файла нет.
        ValueError: расширение не .csv; CSV пустой, без заголовка
            или без строк с данными.
    """
    csv_file = Path(csv_path)

    if not csv_file.exists():
        raise FileNotFoundError(f"Файл не найден: {csv_path}")
    if csv_file.suffix != ".csv":
        raise ValueError(f"Ожидался файл .csv, получен: {csv_file.suffix}")

    with csv_file.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames:
            raise ValueError("CSV пустой или без заголовка")
        rows = list(reader)

    if not rows:
        raise ValueError("В CSV нет строк с данными")

    json_file = Path(json_path)
    json_file.parent.mkdir(parents=True, exist_ok=True)

    with json_file.open("w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    json_to_csv("data/samples/people.json", "data/out/people_from_json.csv")
    csv_to_json("data/samples/people.csv", "data/out/people_from_csv.json")
