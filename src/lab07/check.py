"""ЛР7, задание C: проверка своих функций против эталона на случайных данных.

Эталоны: sorted() для сортировок, list.index() для поиска,
для Two Sum два решения сверяются друг с другом и с условием задачи.
При первом расхождении падает AssertionError с данными, на которых
разошлось. Каждая функция возвращает число выполненных проверок.

Запуск из корня репозитория:
    python -m src.lab07.check
"""

import random

from src.lab07.search import (
    binary_search,
    linear_search,
    two_sum_brute,
    two_sum_fast,
)
from src.lab07.sorting import bubble_sort, insertion_sort, selection_sort


def random_list(max_len: int = 50) -> list[int]:
    """Создаёт случайный список для проверок.

    Args:
        max_len: наибольшая длина списка; длина выбирается от 0
            до max_len включительно, так что бывает и пустой список.

    Returns:
        Список целых от -100 до 100, обычно с повторами.
    """
    n = random.randint(0, max_len)
    return [random.randint(-100, 100) for _ in range(n)]


def check_sorting(fn, trials: int = 100) -> int:
    """Сравнивает сортировку fn с эталоном sorted().

    На каждом прогоне проверяет, что fn(nums) == sorted(nums) и что
    исходный список не изменился. Отдельно проверяет [] и [7].

    Args:
        fn: проверяемая функция сортировки.
        trials: сколько случайных списков проверить.

    Returns:
        Число выполненных проверок: trials + 2.

    Raises:
        AssertionError: при первом расхождении; в сообщении — имя
            функции, входной список и неверный ответ.
    """
    for _ in range(trials):
        nums = random_list()
        original = list(nums)
        result = fn(nums)
        assert result == sorted(nums), (
            f"{fn.__name__} ошиблась на {nums}: {result}"
        )
        assert nums == original, f"{fn.__name__} изменила исходный список"
    assert fn([]) == [], f"{fn.__name__} ошиблась на []"
    assert fn([7]) == [7], f"{fn.__name__} ошиблась на [7]"
    return trials + 2


def check_search(trials: int = 100) -> int:
    """Проверяет linear_search и binary_search на случайных списках.

    linear_search сравнивается с list.index (ValueError соответствует
    -1). binary_search проверяется по свойству ответа, потому что при
    повторах он может вернуть индекс любого вхождения: по найденному
    индексу должен лежать x, а если x в списке нет — ответ -1.
    Отдельно проверяются первый и последний элементы.

    Args:
        trials: сколько случайных списков проверить.

    Returns:
        Число выполненных проверок.

    Raises:
        AssertionError: при первом расхождении, с данными в сообщении.
    """
    count = 0
    for _ in range(trials):
        nums = random_list()
        x = random.randint(-110, 110)

        try:
            expected = nums.index(x)
        except ValueError:
            expected = -1
        got = linear_search(nums, x)
        assert got == expected, (
            f"linear_search({nums}, {x}) = {got}, ожидалось {expected}"
        )
        count += 1

        s = sorted(nums)
        got = binary_search(s, x)
        if x in s:
            assert got != -1 and s[got] == x, (
                f"binary_search({s}, {x}) = {got}"
            )
        else:
            assert got == -1, (
                f"binary_search({s}, {x}) = {got}, ожидалось -1"
            )
        count += 1

        if s:
            for edge in (s[0], s[-1]):
                got = binary_search(s, edge)
                assert got != -1 and s[got] == edge, (
                    f"binary_search({s}, {edge}) = {got}"
                )
                count += 1
    return count


def is_valid_pair(nums: list, target: int, pair: tuple[int, int]) -> bool:
    """Проверяет, что пара индексов — правильный ответ Two Sum.

    Args:
        nums: список чисел.
        target: нужная сумма.
        pair: пара индексов (i, j).

    Returns:
        True, если 0 <= i < j < len(nums) и nums[i] + nums[j] == target.
    """
    i, j = pair
    return 0 <= i < j < len(nums) and nums[i] + nums[j] == target


def check_two_sum(trials: int = 100) -> int:
    """Сверяет two_sum_brute и two_sum_fast между собой и с условием.

    Оба способа должны либо вернуть None, либо вернуть корректные
    пары (возможно, разные: условие допускает любой ответ).

    Args:
        trials: сколько случайных списков проверить.

    Returns:
        Число выполненных проверок: trials.

    Raises:
        AssertionError: при первом расхождении, с данными в сообщении.
    """
    for _ in range(trials):
        nums = random_list(max_len=20)
        target = random.randint(-200, 200)
        brute = two_sum_brute(nums, target)
        fast = two_sum_fast(nums, target)
        where = f"nums={nums}, target={target}"
        if brute is None:
            assert fast is None, f"{where}: brute=None, fast={fast}"
        else:
            assert fast is not None, f"{where}: brute={brute}, fast=None"
            assert is_valid_pair(nums, target, brute), (
                f"two_sum_brute ошиблась: {where}, {brute}"
            )
            assert is_valid_pair(nums, target, fast), (
                f"two_sum_fast ошиблась: {where}, {fast}"
            )
    return trials


def main() -> None:
    """Прогоняет все проверки и печатает «OK: N проверок».

    random.seed(42) делает данные одинаковыми при каждом запуске:
    упавшая проверка упадёт снова на тех же данных.
    """
    random.seed(42)
    total = 0
    for fn in (bubble_sort, insertion_sort, selection_sort):
        total += check_sorting(fn)
    total += check_search()
    total += check_two_sum()
    print(f"OK: {total} проверок")


if __name__ == "__main__":
    main()
