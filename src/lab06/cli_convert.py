"""ЛР6: CLI-конвертеры — подкоманды json2csv, csv2json, csv2xlsx.

Сами конвертации написаны в ЛР5 (src/lab05), здесь только разбор
аргументов и вывод понятных сообщений об ошибках. csv2xlsx использует
функцию из ЛР5, которой нужен openpyxl (pip install -r requirements.txt).

Запуск из корня репозитория:
    python -m src.lab06.cli_convert json2csv --in data/samples/people.json --out data/out/people.csv
    python -m src.lab06.cli_convert csv2json --in data/samples/people.csv --out data/out/people.json
    python -m src.lab06.cli_convert csv2xlsx --in data/samples/people.csv --out data/out/people.xlsx
"""

import argparse
import sys

from src.lab05.csv_xlsx import csv_to_xlsx
from src.lab05.json_csv import csv_to_json, json_to_csv


def main() -> None:
    """Разбирает аргументы командной строки и запускает конвертацию.

    Функции ЛР5 выбрасывают FileNotFoundError и ValueError (в том числе
    UnicodeDecodeError и json.JSONDecodeError — подклассы ValueError);
    они перехватываются и печатаются в stderr.

    Коды выхода: 0 — успех, 1 — ошибка при конвертации,
    2 — неверные аргументы (выставляет argparse).
    """
    parser = argparse.ArgumentParser(description="Конвертеры данных (ЛР6)")
    subparsers = parser.add_subparsers(dest="command", required=True)

    commands = {
        "json2csv": "JSON -> CSV",
        "csv2json": "CSV -> JSON",
        "csv2xlsx": "CSV -> XLSX",
    }
    for name, help_text in commands.items():
        p = subparsers.add_parser(name, help=help_text)
        p.add_argument("--in", dest="input", required=True, help="входной файл")
        p.add_argument("--out", dest="output", required=True, help="выходной файл")

    args = parser.parse_args()

    try:
        if args.command == "json2csv":
            json_to_csv(args.input, args.output)
        elif args.command == "csv2json":
            csv_to_json(args.input, args.output)
        elif args.command == "csv2xlsx":
            csv_to_xlsx(args.input, args.output)
    except (FileNotFoundError, ValueError) as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(1)
    except OSError as e:
        print(
            f"Ошибка: не удалось прочитать или записать файл: {e.strerror}",
            file=sys.stderr,
        )
        sys.exit(1)

    print(f"Готово: {args.input} -> {args.output}")


if __name__ == "__main__":
    main()
