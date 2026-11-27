"""ЛР9, задание B: CLI к CSV-хранилищу студентов.

Подкоманды add, list, find, remove, update вызывают функции из
group.py. Общий параметр --db — путь к хранилищу (по умолчанию
data/lab09/students.csv), пишется до подкоманды.

Запуск из корня репозитория:
    python -m src.lab09.cli_students list --sort gpa
    python -m src.lab09.cli_students add --fio "Иванов Иван" --birthdate 2007-10-10 \
        --group БИВТ-26-6-1 --gpa 4.3
    python -m src.lab09.cli_students find --q иван
    python -m src.lab09.cli_students update --fio "Иванов Иван" --gpa 4.8
    python -m src.lab09.cli_students remove --fio "Иванов Иван"
    python -m src.lab09.cli_students --db data/lab09/other.csv list
"""

import argparse
import sys

from src.lab08.models import format_student
from src.lab09.group import (
    add_student,
    find_students,
    list_students,
    remove_student,
    update_student,
)

DEFAULT_DB = "data/lab09/students.csv"


def main() -> None:
    """Разбирает аргументы и выполняет подкоманду.

    Ошибки данных из group.py (TypeError, ValueError, KeyError)
    печатаются в stderr.

    Коды выхода: 0 — успех; 1 — ошибка данных или студент не найден
    (remove, update); 2 — неверные аргументы (выставляет argparse).
    """
    parser = argparse.ArgumentParser(description="CSV-база студентов (ЛР9)")
    parser.add_argument(
        "--db", default=DEFAULT_DB, help=f"путь к CSV (по умолчанию {DEFAULT_DB})"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    p_add = subparsers.add_parser("add", help="добавить студента")
    p_add.add_argument("--fio", required=True, help="ФИО студента")
    p_add.add_argument("--birthdate", required=True, help="дата рождения ГГГГ-ММ-ДД")
    p_add.add_argument("--group", required=True, help="группа студента")
    p_add.add_argument("--gpa", required=True, type=float, help="средний балл 0..5")

    p_list = subparsers.add_parser("list", help="список студентов")
    p_list.add_argument("--sort", choices=["fio", "gpa"], help="поле сортировки")

    p_find = subparsers.add_parser("find", help="поиск по подстроке в ФИО")
    p_find.add_argument("--q", required=True, help="подстрока, регистр не важен")

    p_remove = subparsers.add_parser("remove", help="удалить всех студентов с этим ФИО")
    p_remove.add_argument("--fio", required=True, help="ФИО студента")

    p_update = subparsers.add_parser("update", help="обновить поля студента")
    p_update.add_argument("--fio", required=True, help="ФИО студента")
    p_update.add_argument("--group", help="новая группа")
    p_update.add_argument("--birthdate", help="новая дата рождения ГГГГ-ММ-ДД")
    p_update.add_argument("--gpa", type=float, help="новый средний балл")

    args = parser.parse_args()

    try:
        if args.command == "add":
            student = {
                "fio": args.fio,
                "birthdate": args.birthdate,
                "group": args.group,
                "gpa": args.gpa,
            }
            add_student(args.db, student)
            print(f"Студент {args.fio} добавлен.")

        elif args.command == "list":
            students = list_students(args.db, args.sort)
            if not students:
                print("База пуста.")
            for student in students:
                print(format_student(student))

        elif args.command == "find":
            students = find_students(args.db, args.q)
            if not students:
                print("Студенты не найдены.")
            for student in students:
                print(format_student(student))

        elif args.command == "remove":
            removed = remove_student(args.db, args.fio)
            if not removed:
                print(f"Ошибка: студент {args.fio!r} не найден", file=sys.stderr)
                sys.exit(1)
            print(f"Удалено записей: {removed}")

        elif args.command == "update":
            fields = {"group": args.group, "birthdate": args.birthdate, "gpa": args.gpa}
            fields = {k: v for k, v in fields.items() if v is not None}
            if not update_student(args.db, args.fio, **fields):
                print(f"Ошибка: студент {args.fio!r} не найден", file=sys.stderr)
                sys.exit(1)
            print(f"Студент {args.fio} обновлён.")

    except (TypeError, ValueError, KeyError) as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
