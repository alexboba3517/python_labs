"""ЛР7, задание A: поиск в списке и задача Two Sum.

linear_search  — O(n), работает на любом списке.
binary_search  — O(log n), только на отсортированном по возрастанию.
two_sum_brute  — перебор всех пар, O(n²).
two_sum_fast   — один проход со словарём, O(n).

«Не нашли» поиск сообщает через -1, Two Sum — через None.
Входные списки функции не меняют.
"""


def linear_search(nums: list, x) -> int:
    """Ищет x, просматривая список слева направо.

    Args:
        nums: список, в котором ищем; порядок элементов любой.
        x: искомое значение.

    Returns:
        Индекс первого вхождения x или -1, если x в списке нет.

    >>> linear_search([4, 2, 7, 2], 2)
    1
    >>> linear_search([4, 2, 7, 2], 9)
    -1
    >>> linear_search([], 1)
    -1
    """
    for i in range(len(nums)):
        if nums[i] == x:
            return i
    return -1


def binary_search(sorted_nums: list, x) -> int:
    """Ищет x делением отрезка пополам.

    Инвариант цикла: если x есть в списке, он лежит между lo и hi
    включительно. На неотсортированном списке результат не определён:
    функция не упадёт, но может не найти x, который в списке есть.

    Args:
        sorted_nums: список, отсортированный по возрастанию.
        x: искомое значение.

    Returns:
        Индекс x или -1, если x в списке нет. При повторах — индекс
        любого из вхождений.

    >>> binary_search([1, 3, 5, 7], 5)
    2
    >>> binary_search([1, 3, 5, 7], 4)
    -1
    >>> binary_search([5], 5)
    0
    >>> binary_search([], 5)
    -1
    """
    lo = 0
    hi = len(sorted_nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if sorted_nums[mid] == x:
            return mid
        if sorted_nums[mid] < x:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1


def two_sum_brute(nums: list, target) -> tuple[int, int] | None:
    """Ищет пару с суммой target перебором всех пар i < j.

    Args:
        nums: список чисел.
        target: нужная сумма.

    Returns:
        Пару индексов (i, j), где i < j и nums[i] + nums[j] == target,
        или None, если такой пары нет. При нескольких ответах — пара
        с наименьшим i.

    >>> two_sum_brute([2, 7, 11, 15], 9)
    (0, 1)
    >>> two_sum_brute([1, 2], 10) is None
    True
    """
    n = len(nums)
    for i in range(n):
        for j in range(i + 1, n):
            if nums[i] + nums[j] == target:
                return (i, j)
    return None


def two_sum_fast(nums: list, target) -> tuple[int, int] | None:
    """Ищет пару с суммой target за один проход со словарём.

    В словаре seen хранится «значение -> индекс» для уже просмотренных
    элементов. Для очередного числа проверяем, встречалось ли
    target - число. Проверка идёт до добавления, поэтому элемент
    не встанет в пару сам с собой.

    Args:
        nums: список чисел.
        target: нужная сумма.

    Returns:
        Пару индексов (i, j), где i < j и nums[i] + nums[j] == target,
        или None. При нескольких ответах может вернуть не ту пару,
        что two_sum_brute: условие допускает любую.

    >>> two_sum_fast([2, 7, 11, 15], 9)
    (0, 1)
    >>> two_sum_fast([3, 3], 6)
    (0, 1)
    >>> two_sum_fast([3], 6) is None
    True
    """
    seen = {}
    for j in range(len(nums)):
        need = target - nums[j]
        if need in seen:
            return (seen[need], j)
        seen[nums[j]] = j
    return None
