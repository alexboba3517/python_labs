"""ЛР7, задание D: замеры времени через timeit.

Сортировки:  свои три против sorted на n = 1 000 / 10 000 / 100 000.
Поиск:       10 000 запросов к списку из 100 000; для бинарного
             время предварительной сортировки — отдельной строкой.
Two Sum:     перебор против словаря на n = 1 000 / 10 000.

Все алгоритмы в одной задаче получают одни и те же данные,
random.seed(42) делает результаты повторяемыми. Квадратичные
сортировки на 10^5 не запускаются (см. SKIP_ABOVE).

Как мерим (правила из Л8): быстрые операции — 5 повторов по 10
запусков, берём минимум и делим на 10; всё сверх минимума — помехи
системы. Медленные (секунды и больше) — один запуск: там помехи
в миллисекунды на результат не влияют, а повторы стоили бы минут.

Результат — таблица в консоль и data/lab07/bench.csv.
Запуск из корня репозитория:
    python -m src.lab07.bench
"""

import random
import timeit

from src.lab04.io_txt_csv import write_csv
from src.lab07.search import (
    binary_search,
    linear_search,
    two_sum_brute,
    two_sum_fast,
)
from src.lab07.sorting import bubble_sort, insertion_sort, selection_sort

CSV_PATH = "data/lab07/bench.csv"
SORT_SIZES = [1_000, 10_000, 100_000]
TWO_SUM_SIZES = [1_000, 10_000]
SKIP_ABOVE = 10_000
ONE_RUN_FROM = 10_000
REPEAT = 5
NUMBER = 10


def measure(fn, slow: bool = False) -> float:
    """Измеряет время одного запуска fn().

    Args:
        fn: функция без аргументов (на практике lambda), которую мерим.
        slow: False — timeit.repeat делает REPEAT серий по NUMBER
            запусков, берём лучшую серию и делим на NUMBER.
            True — один запуск, для операций, которые идут секунды.

    Returns:
        Время одного запуска в секундах.
    """
    if slow:
        return timeit.timeit(fn, number=1)
    return min(timeit.repeat(fn, number=NUMBER, repeat=REPEAT)) / NUMBER


def bench_sorts() -> list[tuple]:
    """Замеряет три свои сортировки и sorted на n из SORT_SIZES.

    Для каждого n список генерируется один раз, и все сортировки
    получают одни и те же данные. Сортировки не меняют исходный список,
    поэтому замеры не влияют друг на друга.

    Returns:
        Строки таблицы (task, n, impl, seconds); вместо времени
        квадратичных сортировок на n > SKIP_ABOVE — строка "> 60".
    """
    rows = []
    for n in SORT_SIZES:
        data = [random.randint(0, 1_000_000) for _ in range(n)]
        rows.append(("sort", n, "sorted", measure(lambda: sorted(data))))
        for fn in (bubble_sort, insertion_sort, selection_sort):
            if n > SKIP_ABOVE:
                rows.append(("sort", n, fn.__name__, "> 60"))
            else:
                t = measure(lambda: fn(data), slow=(n >= ONE_RUN_FROM))
                rows.append(("sort", n, fn.__name__, t))
    return rows


def bench_search() -> list[tuple]:
    """Замеряет 10 000 запросов к списку из 100 000 чисел.

    Примерно 40 % запросов в списке есть. Время сортировки перед
    бинарным поиском записывается отдельной строкой sort_for_binary:
    без неё бинарный поиск не работает, и честно учитывать её цену.

    Returns:
        Три строки таблицы: linear_search, sort_for_binary,
        binary_search.
    """
    n = 100_000
    data = [random.randint(0, 200_000) for _ in range(n)]
    queries = [random.randint(0, 200_000) for _ in range(10_000)]

    t_linear = measure(
        lambda: [linear_search(data, q) for q in queries], slow=True
    )
    t_sort = measure(lambda: sorted(data))
    s = sorted(data)
    t_binary = measure(lambda: [binary_search(s, q) for q in queries])

    return [
        ("search", n, "linear_search", t_linear),
        ("search", n, "sort_for_binary", t_sort),
        ("search", n, "binary_search", t_binary),
    ]


def bench_two_sum() -> list[tuple]:
    """Замеряет two_sum_brute и two_sum_fast на n из TWO_SUM_SIZES.

    Данные: n - 2 случайных числа до 10^6 и два больших в конце.
    Сумма двух больших больше любой другой суммы пары, поэтому ответ
    существует, он единственный и стоит в самом конце: перебор
    проверит все пары — это худший случай.

    Returns:
        Строки таблицы (task, n, impl, seconds), по две на каждое n.
    """
    rows = []
    for n in TWO_SUM_SIZES:
        nums = [random.randint(0, 1_000_000) for _ in range(n - 2)]
        nums += [10_000_000, 10_000_001]
        target = 20_000_001
        t_brute = measure(
            lambda: two_sum_brute(nums, target), slow=(n >= ONE_RUN_FROM)
        )
        t_fast = measure(lambda: two_sum_fast(nums, target))
        rows.append(("two_sum", n, "two_sum_brute", t_brute))
        rows.append(("two_sum", n, "two_sum_fast", t_fast))
    return rows


def format_seconds(t: float | str) -> str:
    """Форматирует время для таблицы.

    Args:
        t: время в секундах или строка вида "> 60".

    Returns:
        Число с 6 знаками после точки; строку — без изменений.
    """
    if isinstance(t, str):
        return t
    return f"{t:.6f}"


def main() -> None:
    """Запускает все замеры, печатает таблицу и пишет её в CSV_PATH."""
    random.seed(42)
    rows = bench_sorts() + bench_search() + bench_two_sum()
    rows = [(task, n, impl, format_seconds(t)) for task, n, impl, t in rows]

    print(f"{'task':<8} {'n':>7}  {'impl':<16} {'seconds':>12}")
    print("-" * 47)
    for task, n, impl, t in rows:
        print(f"{task:<8} {n:>7}  {impl:<16} {t:>12}")

    write_csv(rows, CSV_PATH, header=("task", "n", "impl", "seconds"))
    print(f"\nСохранено: {CSV_PATH}")


if __name__ == "__main__":
    main()
