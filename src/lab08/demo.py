"""ЛР8: запуск модели и сериализации на файлах из data/lab08.

Запуск из корня репозитория:
    python -m src.lab08.demo
"""

from src.lab08.models import format_student
from src.lab08.serialize import students_from_json, students_to_json

INPUT_JSON = "data/lab08/students_input.json"
OUTPUT_JSON = "data/lab08/students_output.json"
BAD_JSON = "data/lab08/students_bad.json"


def main() -> None:
    students = students_from_json(INPUT_JSON)
    for s in students:
        print(format_student(s))
    students_to_json(students, OUTPUT_JSON)
    print(f"записано {len(students)} -> {OUTPUT_JSON}")
    print("прочитали обратно, совпадает:", students_from_json(OUTPUT_JSON) == students)

    print()
    good = students_from_json(BAD_JSON)
    print(f"корректных записей: {len(good)}")


if __name__ == "__main__":
    main()
