def format_record(rec: tuple[str, str, float]) -> str:
    """Форматирует запись студента в строку "Фамилия И.О., гр. ГРУППА, GPA X.XX".

    Запись — кортеж (ФИО, группа, GPA). ФИО может состоять из 2 или 3 слов,
    лишние пробелы и регистр букв исправляются. GPA выводится с двумя
    знаками после запятой.

    Args:
        rec: кортеж (fio, group, gpa).

    Returns:
        Отформатированная строка.

    Raises:
        TypeError: если rec не кортеж, ФИО или группа не строки,
            GPA не число.
        ValueError: если в записи не 3 поля, ФИО или группа пустые,
            в ФИО не 2 и не 3 слова, GPA вне диапазона от 0 до 5.

    Examples:
        >>> format_record(("Иванов Иван Иванович", "BIVT-25", 4.6))
        'Иванов И.И., гр. BIVT-25, GPA 4.60'
        >>> format_record(("Петров Пётр", "IKBO-12", 5.0))
        'Петров П., гр. IKBO-12, GPA 5.00'
        >>> format_record(("Петров Пётр Петрович", "IKBO-12", 5.0))
        'Петров П.П., гр. IKBO-12, GPA 5.00'
        >>> format_record(("  сидорова  анна   сергеевна ", "ABB-01", 3.999))
        'Сидорова А.С., гр. ABB-01, GPA 4.00'
        >>> format_record(("   ", "ABB-01", 4.0))
        Traceback (most recent call last):
            ...
        ValueError: format_record: пустое ФИО
    """
    if not isinstance(rec, tuple):
        raise TypeError("format_record: запись должна быть кортежем")
    if len(rec) != 3:
        raise ValueError("format_record: в записи должно быть 3 поля")

    fio, group, gpa = rec

    if not isinstance(fio, str) or not isinstance(group, str):
        raise TypeError("format_record: ФИО и группа должны быть строками")
    if isinstance(gpa, bool) or not isinstance(gpa, (int, float)):
        raise TypeError("format_record: GPA должен быть числом")

    parts = fio.split()
    group = group.strip()
    if not parts:
        raise ValueError("format_record: пустое ФИО")
    if len(parts) not in (2, 3):
        raise ValueError("format_record: в ФИО должно быть 2 или 3 слова")
    if not group:
        raise ValueError("format_record: пустая группа")
    if not 0 <= gpa <= 5:
        raise ValueError("format_record: GPA должен быть от 0 до 5")

    surname = parts[0].capitalize()
    initials = ""
    for name in parts[1:]:
        initials += name[0].upper() + "."

    return f"{surname} {initials}, гр. {group}, GPA {gpa:.2f}"


if __name__ == "__main__":
    print("format_record:")
    for rec in [
        ("Иванов Иван Иванович", "BIVT-25", 4.6),
        ("Петров Пётр", "IKBO-12", 5.0),
        ("Петров Пётр Петрович", "IKBO-12", 5.0),
        ("  сидорова  анна   сергеевна ", "ABB-01", 3.999),
    ]:
        print(f"  {rec} -> {format_record(rec)}")