"""ЛР7, задание B: три квадратичные сортировки.

Каждая функция возвращает НОВЫЙ список, отсортированный по возрастанию,
и не меняет исходный: в начале делается копия nums = list(nums).
Готовые sorted, .sort(), min, max внутри не используются.
"""


def bubble_sort(nums: list) -> list:
    """Сортировка пузырьком, O(n²); на отсортированном списке O(n).

    За один проход соседние элементы меняются местами, если стоят
    не по порядку, и максимум «всплывает» в конец. Если за проход
    не было ни одного обмена, список уже отсортирован — выходим раньше.

    Args:
        nums: список (или любой перебираемый объект) сравнимых значений.

    Returns:
        Новый список, отсортированный по возрастанию.

    >>> bubble_sort([3, 1, 2])
    [1, 2, 3]
    >>> bubble_sort([2, 2, 1])
    [1, 2, 2]
    >>> bubble_sort([])
    []
    """
    nums = list(nums)
    n = len(nums)
    for i in range(n - 1):
        swapped = False
        for j in range(n - 1 - i):
            if nums[j] > nums[j + 1]:
                nums[j], nums[j + 1] = nums[j + 1], nums[j]
                swapped = True
        if not swapped:
            break
    return nums


def insertion_sort(nums: list) -> list:
    """Сортировка вставками, O(n²); на почти отсортированном почти O(n).

    Слева растёт отсортированная часть. Очередной элемент сдвигается
    влево, пока слева от него стоит больший.

    Args:
        nums: список (или любой перебираемый объект) сравнимых значений.

    Returns:
        Новый список, отсортированный по возрастанию.

    >>> insertion_sort([3, 1, 2])
    [1, 2, 3]
    >>> insertion_sort([5])
    [5]
    """
    nums = list(nums)
    for i in range(1, len(nums)):
        current = nums[i]
        j = i - 1
        while j >= 0 and nums[j] > current:
            nums[j + 1] = nums[j]
            j -= 1
        nums[j + 1] = current
    return nums


def selection_sort(nums: list) -> list:
    """Сортировка выбором, O(n²) всегда, даже на отсортированном.

    На шаге i ищем минимум в части nums[i:] и меняем его местами
    с nums[i]. Обменов не больше n - 1. Сортировка неустойчивая.

    Args:
        nums: список (или любой перебираемый объект) сравнимых значений.

    Returns:
        Новый список, отсортированный по возрастанию.

    >>> selection_sort([3, 1, 2])
    [1, 2, 3]
    >>> selection_sort([-1, 5, -1, 0])
    [-1, -1, 0, 5]
    """
    nums = list(nums)
    n = len(nums)
    for i in range(n - 1):
        min_idx = i
        for j in range(i + 1, n):
            if nums[j] < nums[min_idx]:
                min_idx = j
        nums[i], nums[min_idx] = nums[min_idx], nums[i]
    return nums
