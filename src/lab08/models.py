"""ЛР8, задание A: модель Student — запись-словарь без классов.

Запись — словарь ровно с ключами STUDENT_FIELDS:
    fio        str    ФИО, непустая строка
    birthdate  str    дата рождения ГГГГ-ММ-ДД, существует, не в будущем
    group      str    группа, непустая строка
    gpa        float  средний балл от 0 до 5

Записи создаются через make_student или student_from_dict: обе
проверяют данные. Не тот тип — TypeError, не то значение — ValueError;
в сообщении поле, что ждали и что получили.
"""

from datetime import date

STUDENT_FIELDS = ("fio", "birthdate", "group", "gpa")


def make_student(fio, birthdate, group, gpa) -> dict:
    """Собирает запись студента и проверяет каждое поле.

    Args:
        fio: ФИО, например "Иванов Иван Иванович".
        birthdate: дата рождения строкой ГГГГ-ММ-ДД.
        group: группа, например "БИВТ-26-6-1".
        gpa: средний балл, int или float от 0 до 5.

    Returns:
        Запись-словарь; gpa в ней всегда float.

    Raises:
        TypeError, ValueError: поле не прошло проверку (см. validate_student).

    >>> make_student("Иванов Иван Иванович", "2007-05-14", "БИВТ-26-6-1", 4)
    {'fio': 'Иванов Иван Иванович', 'birthdate': '2007-05-14', 'group': 'БИВТ-26-6-1', 'gpa': 4.0}
    """
    rec = {"fio": fio, "birthdate": birthdate, "group": group, "gpa": gpa}
    validate_student(rec)
    rec["gpa"] = float(gpa)
    return rec


def validate_student(rec: dict) -> None:
    """Проверяет запись: набор ключей и значение каждого поля.

    Дата проверяется в два шага: date.fromisoformat отсекает
    несуществующие дни, а сравнение born.isoformat() == birthdate —
    другие формы записи вроде "20070514", которые fromisoformat
    тоже принимает.

    Raises:
        TypeError: rec не словарь или у поля не тот тип.
        ValueError: нет нужного ключа, есть лишний или значение
            не подходит (пустая строка, нет такой даты, gpa вне 0..5).

    >>> validate_student({"fio": "Иванов Иван", "birthdate": "2007-02-30",
    ...                   "group": "БИВТ-26-6-1", "gpa": 4.3})
    Traceback (most recent call last):
    ...
    ValueError: birthdate: ожидалась дата ГГГГ-ММ-ДД, получено '2007-02-30'
    >>> validate_student({"fio": "Иванов Иван", "birthdate": "2007-05-14",
    ...                   "group": "БИВТ-26-6-1", "gpa": 7})
    Traceback (most recent call last):
    ...
    ValueError: gpa: ожидалось 0..5, получено 7
    >>> validate_student({"fio": "Иванов Иван", "birthdate": "2007-05-14",
    ...                   "group": "БИВТ-26-6-1", "gpa": True})
    Traceback (most recent call last):
    ...
    TypeError: gpa: ожидалось число, получено True
    """
    if type(rec) is not dict:
        raise TypeError(f"ожидался словарь, получено {rec!r}")
    for key in STUDENT_FIELDS:
        if key not in rec:
            raise ValueError(f"нет поля {key!r}")
    for key in rec:
        if key not in STUDENT_FIELDS:
            raise ValueError(f"лишнее поле {key!r}")

    for key in ("fio", "group"):
        value = rec[key]
        if type(value) is not str:
            raise TypeError(f"{key}: ожидалась строка, получено {value!r}")
        if not value.strip():
            raise ValueError(f"{key}: ожидалась непустая строка, получено {value!r}")

    birthdate = rec["birthdate"]
    if type(birthdate) is not str:
        raise TypeError(f"birthdate: ожидалась строка, получено {birthdate!r}")
    try:
        born = date.fromisoformat(birthdate)
    except ValueError:
        raise ValueError(
            f"birthdate: ожидалась дата ГГГГ-ММ-ДД, получено {birthdate!r}"
        ) from None
    if born.isoformat() != birthdate:
        raise ValueError(
            f"birthdate: ожидалась дата ГГГГ-ММ-ДД, получено {birthdate!r}"
        )
    if born > date.today():
        raise ValueError(f"birthdate: дата в будущем: {birthdate!r}")

    gpa = rec["gpa"]
    if type(gpa) not in (int, float):
        raise TypeError(f"gpa: ожидалось число, получено {gpa!r}")
    if not 0 <= gpa <= 5:
        raise ValueError(f"gpa: ожидалось 0..5, получено {gpa!r}")


def student_age(rec: dict, today: date | None = None) -> int:
    """Считает полных лет на дату today (по умолчанию — сегодня).

    Разность годов минус 1, если в году today день рождения
    ещё не наступил.

    >>> s = make_student("Петров Пётр", "2007-09-20", "БИВТ-26-6-1", 4.0)
    >>> student_age(s, today=date(2026, 9, 19))
    18
    >>> student_age(s, today=date(2026, 9, 20))
    19
    """
    born = date.fromisoformat(rec["birthdate"])
    if today is None:
        today = date.today()
    elif type(today) is not date:
        raise TypeError(f"today: ожидалась дата (date), получено {today!r}")
    born = date.fromisoformat(rec["birthdate"])
    age = today.year - born.year
    if (today.month, today.day) < (born.month, born.day):
        age -= 1
    return age


def _years_word(n: int) -> str:
    """Слово после числа: 1 год, 3 года, 11 лет, 21 год."""
    if n % 10 == 1 and n % 100 != 11:
        return "год"
    if 2 <= n % 10 <= 4 and not 12 <= n % 100 <= 14:
        return "года"
    return "лет"


def format_student(rec: dict) -> str:
    """Строка вида 'Иванов И.И. (БИВТ-26-6-1), 19 лет, GPA 4.30'.

    Инициалы — первые буквы всех слов ФИО, кроме первого (как в ЛР1).
    Возраст считается на сегодня.
    """
    parts = rec["fio"].split()
    initials = "".join(word[0] + "." for word in parts[1:])
    name = f"{parts[0]} {initials}".rstrip()
    age = student_age(rec)
    return f"{name} ({rec['group']}), {age} {_years_word(age)}, GPA {rec['gpa']:.2f}"


def student_to_dict(rec: dict) -> dict:
    """Проверяет запись и возвращает её копию для сериализации.

    Копия — новый словарь: изменения в нём не затрагивают rec.

    >>> s = make_student("Иванов Иван", "2007-05-14", "БИВТ-26-6-1", 4.3)
    >>> d = student_to_dict(s)
    >>> d == s, d is s
    (True, False)
    """
    validate_student(rec)
    return dict(rec)


def student_from_dict(d: dict) -> dict:
    """Делает запись из словаря, прочитанного из JSON.

    Берёт из d только ключи STUDENT_FIELDS: лишние отбрасываются,
    отсутствующий — ошибка. Дальше — make_student: проверка и gpa -> float.

    >>> student_from_dict({"gpa": 5, "group": "БИВТ-26-6-1", "fio": "Иванов Иван",
    ...                    "birthdate": "2007-05-14", "email": "i@misis.ru"})
    {'fio': 'Иванов Иван', 'birthdate': '2007-05-14', 'group': 'БИВТ-26-6-1', 'gpa': 5.0}
    """
    if type(d) is not dict:
        raise TypeError(f"ожидался объект JSON, получено {d!r}")
    for key in STUDENT_FIELDS:
        if key not in d:
            raise ValueError(f"нет поля {key!r}")
    return make_student(d["fio"], d["birthdate"], d["group"], d["gpa"])
