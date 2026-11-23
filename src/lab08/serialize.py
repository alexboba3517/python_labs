"""ЛР8, задание B: сохранение и загрузка списка студентов в JSON.

JSON — массив объектов с ключами STUDENT_FIELDS, ensure_ascii=False,
indent=2. Каждая прочитанная запись проходит student_from_dict.

Политика для битых записей — skip: битая запись пропускается,
в конце в консоль выводится, сколько записей пропущено и почему
(номер записи с 1 и причина). Так в файле видны все ошибки за один
запуск, а не по одной.
"""

import json
from pathlib import Path

from src.lab08.models import student_from_dict, student_to_dict


def students_to_json(students: list[dict], path: str) -> None:
    """Сохраняет список записей в JSON-файл.

    Все записи проверяются и копируются (student_to_dict) до открытия
    файла: если какая-то битая, старый файл не затрётся. Папка
    создаётся, если её нет.
    """
    data = [student_to_dict(s) for s in students]
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def students_from_json(path: str) -> list[dict]:
    """Читает записи из JSON-файла, битые пропускает (политика skip).

    Returns:
        Список корректных записей.

    Raises:
        FileNotFoundError: файла нет.
        json.JSONDecodeError: файл — не JSON (подкласс ValueError).
        TypeError: в файле не массив.
    """
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    if type(data) is not list:
        raise TypeError(f"{path}: ожидался JSON-массив, получено {type(data).__name__}")

    students = []
    errors = []
    for number, item in enumerate(data, start=1):
        try:
            students.append(student_from_dict(item))
        except (TypeError, ValueError) as e:
            errors.append(f"запись {number}: {e}")

    if errors:
        print(f"{path}: пропущено {len(errors)} из {len(data)}")
        for line in errors:
            print(f"  {line}")
    return students
