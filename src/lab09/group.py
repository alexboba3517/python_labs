"""ЛР9, задание A: «база данных» студентов на CSV — хранилище и CRUD.

Файл хранилища — CSV с заголовком fio,birthdate,group,gpa
(STUDENT_FIELDS из ЛР8), одна строка — один студент.

Классов нет: каждая функция получает путь к CSV первым аргументом.
CSV нельзя поменять построчно на месте, поэтому изменяющие операции
(add, remove, update) устроены одинаково: загрузить весь файл в
список -> изменить список в памяти -> перезаписать файл целиком.
Читающие операции (list, find) файл не меняют.

Каждая строка при чтении проходит student_from_dict из ЛР8, каждая
новая или изменённая запись проверяется до сохранения. Ошибки
данных — ValueError (или TypeError от ЛР8), неизвестное поле
в update_student — KeyError.
"""

import csv
from pathlib import Path

from src.lab08.models import STUDENT_FIELDS, student_from_dict, validate_student


def ensure_storage(path) -> None:
    """Создаёт CSV-хранилище с одним заголовком, если файла ещё нет.

    Существующий файл не трогается: режим "w" стёр бы его. Недостающие
    папки создаются.

    Raises:
        ValueError: по пути лежит не файл (например, папка).
    """
    out = Path(path)
    if out.exists():
        if not out.is_file():
            raise ValueError(f"{path}: путь существует, но это не файл")
        return
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=STUDENT_FIELDS)
        writer.writeheader()


def load_students(path) -> list[dict]:
    """Читает все записи из CSV-хранилища.

    Если файла нет, он создаётся (ensure_storage) и возвращается [].
    Из CSV всё приходит строками, поэтому gpa переводится во float
    до student_from_dict: validate_student из ЛР8 строку не примет.

    DictReader не падает, если в строке не столько значений, сколько
    колонок: лишние кладёт в ключ None, недостающим полям ставит
    значение None. Оба случая проверяются явно.

    Битая строка — ошибка, а не пропуск: иначе следующий save_students
    молча удалил бы её из файла.

    Returns:
        Список записей; gpa в них — float.

    Raises:
        ValueError: нет заголовка или он не fio,birthdate,group,gpa;
            в строке лишние, недостающие или пустые значения; запись
            не прошла проверку ЛР8. В сообщении — номер строки файла.
    """
    ensure_storage(path)
    with open(path, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames != list(STUDENT_FIELDS):
            got = ",".join(reader.fieldnames) if reader.fieldnames else "пустой файл"
            raise ValueError(
                f"{path}: ожидался заголовок {','.join(STUDENT_FIELDS)}, получено {got}"
            )
        students = []
        for n, row in enumerate(reader, start=2):  # строка 1 — заголовок
            if None in row:
                raise ValueError(f"{path}, строка {n}: лишние значения {row[None]}")
            if None in row.values():
                raise ValueError(f"{path}, строка {n}: не хватает значений")
            if "" in row.values():
                raise ValueError(f"{path}, строка {n}: пустое значение")
            try:
                row["gpa"] = float(row["gpa"])
                student = student_from_dict(row)
            except (ValueError, TypeError) as e:
                raise ValueError(f"{path}, строка {n}: {e}") from None
            students.append(student)
    return students


def save_students(path, students) -> None:
    """Перезаписывает CSV-хранилище целиком: заголовок и все записи.

    Все записи проверяются до открытия файла: open(..., "w") сразу
    очищает файл, и ошибка на середине записи потеряла бы остальных
    студентов. Папка создаётся, если её нет.

    Raises:
        TypeError, ValueError: какая-то запись не прошла validate_student;
            файл при этом не изменился.
    """
    for student in students:
        validate_student(student)
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=STUDENT_FIELDS)
        writer.writeheader()
        writer.writerows(students)


def add_student(path, student: dict) -> None:
    """Create: проверяет запись и дописывает её в конец хранилища.

    student_from_dict и проверяет запись, и приводит gpa к float,
    поэтому в файле gpa всегда вида 4.0, а не 4.

    Raises:
        TypeError, ValueError: запись не прошла проверку ЛР8; файл
            при этом даже не читается.
    """
    student = student_from_dict(student)
    students = load_students(path)
    students.append(student)
    save_students(path, students)


def list_students(path, sort_by=None) -> list[dict]:
    """Read: все записи; sort_by=None — в порядке файла.

    sorted стабильный: записи с равным ключом (например, одинаковым
    gpa) остаются в том порядке, в каком были в файле.

    Args:
        sort_by: None, "fio" или "gpa".

    Raises:
        ValueError: sort_by не из {None, "fio", "gpa"}; проверяется
            до чтения файла.
    """
    if sort_by not in (None, "fio", "gpa"):
        raise ValueError(f"sort_by: ожидалось fio или gpa, получено {sort_by!r}")
    students = load_students(path)
    if sort_by is None:
        return students
    return sorted(students, key=lambda s: s[sort_by])


def find_students(path, substr: str) -> list[dict]:
    """Read: записи, у которых substr входит в fio без учёта регистра.

    В нижний регистр приводятся обе стороны: и запрос, и ФИО.
    """
    query = substr.lower()
    return [s for s in load_students(path) if query in s["fio"].lower()]


def remove_student(path, fio: str) -> int:
    """Delete: удаляет все записи с fio (точное совпадение).

    Удаление через новый список, а не pop в цикле: pop внутри for
    сдвигает элементы, и цикл перескакивает соседнюю запись.
    Если удалять некого, файл не перезаписывается.

    Returns:
        Сколько записей удалено.
    """
    students = load_students(path)
    kept = [s for s in students if s["fio"] != fio]
    removed = len(students) - len(kept)
    if removed > 0:
        save_students(path, kept)
    return removed


def update_student(path, fio: str, **fields) -> bool:
    """Update: меняет поля первой записи с fio.

    Обновляется копия записи, проверяется и только потом встаёт в
    список и сохраняется: битые новые значения не попадут в файл.

    Args:
        fields: новые значения, например gpa=4.5, group="БИВТ-26-6-2".

    Returns:
        True, если запись найдена и обновлена, иначе False.

    Raises:
        KeyError: ключа нет в STUDENT_FIELDS; проверяется до чтения файла.
        TypeError, ValueError: обновлённая запись не прошла проверку ЛР8.
    """
    for key in fields:
        if key not in STUDENT_FIELDS:
            allowed = ", ".join(STUDENT_FIELDS)
            raise KeyError(f"неизвестное поле {key!r}, ожидалось одно из {allowed}")
    students = load_students(path)
    for i, s in enumerate(students):
        if s["fio"] == fio:
            updated = dict(s)
            updated.update(fields)
            students[i] = student_from_dict(updated)
            save_students(path, students)
            return True
    return False
