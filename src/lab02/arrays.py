def min_max(nums: list[float | int]) -> tuple[float | int, float | int]:
    """Возвращает кортеж (минимум, максимум) для списка чисел.

    Проходит по списку один раз, начиная оба значения с первого элемента.
    Встроенные min() и max() не используются. Входной список не изменяется.

    Args:
        nums: непустой список чисел (int или float).

    Returns:
        Кортеж (min, max).

    Raises:
        ValueError: если список пустой.

    Examples:
        >>> min_max([3, -1, 5, 5, 0])
        (-1, 5)
        >>> min_max([42])
        (42, 42)
        >>> min_max([-5, -2, -9])
        (-9, -2)
        >>> min_max([1.5, 2, 2.0, -3.1])
        (-3.1, 2)
        >>> min_max([])
        Traceback (most recent call last):
            ...
        ValueError: min_max: список пуст
    """
    if len(nums) == 0:
        raise ValueError("min_max: список пуст")
    mn = nums[0]
    mx = nums[0]
    for x in nums:
        if x < mn:
            mn = x
        elif x > mx:
            mx = x
    return (mn, mx)


def unique_sorted(nums: list[float | int]) -> list[float | int]:
    """Возвращает отсортированный по возрастанию список уникальных значений.

    Сначала убирает повторы через set(), затем на каждом шаге находит
    минимум оставшихся (через min_max), добавляет его в результат и
    удаляет из рабочего списка. Встроенные sorted() и .sort() не
    используются. Входной список не изменяется.

    Args:
        nums: список чисел (int или float), может быть пустым.

    Returns:
        Новый список уникальных значений по возрастанию.
        Для пустого списка — пустой список.

    Examples:
        >>> unique_sorted([3, 1, 2, 1, 3])
        [1, 2, 3]
        >>> unique_sorted([])
        []
        >>> unique_sorted([-1, -1, 0, 2, 2])
        [-1, 0, 2]
        >>> unique_sorted([1.0, 1, 2.5, 2.5, 0])
        [0, 1.0, 2.5]
    """
    result = []
    nums_s = list(set(nums))
    for _ in range(len(nums_s)):
        smallest = min_max(nums_s)[0]
        result.append(smallest)
        nums_s.remove(smallest)
    return result


def flatten(mat: list[list | tuple]) -> list:
    """Возвращает одномерный список, состоящий из всех элементов матрицы.
    
    Args:
        mat: матрица (список списков или кортежей).

    Returns:
        Одномерный список элементов матрицы.
    
    Raises:
        TypeError: если матрица содержит элементы, не являющиеся списками или кортежами.
    
     Examples:
            >>> flatten([[1, 2], [3, 4]])
            [1, 2, 3, 4]
            >>> flatten([[1, 2], (3, 4, 5)])
            [1, 2, 3, 4, 5]
            >>> flatten([[1], [], [2, 3]])
            [1, 2, 3]
            >>> flatten([[1, 2], "ab"])
            Traceback (most recent call last):
                ...
            TypeError: flatten: матрица должна состоять из списков или кортежей
    """
    result = []
    for row in mat:
        if isinstance(row, (list, tuple)):
            for x in row:
                result.append(x)
        else:
            raise TypeError("flatten: матрица должна состоять из списков или кортежей")
    return result


if __name__ == "__main__":
    print("min_max:")
    for nums in [[3, -1, 5, 5, 0], [42], [-5, -2, -9], [1.5, 2, 2.0, -3.1]]:
        print(f"  {nums} -> {min_max(nums)}")

    print("unique_sorted:")
    for nums in [[3, 1, 2, 1, 3], [], [-1, -1, 0, 2, 2], [1.0, 1, 2.5, 2.5, 0]]:
        print(f"  {nums} -> {unique_sorted(nums)}")

    print("flatten:")
    for mat in [[[1, 2], [3, 4]], [[1, 2], (3, 4, 5)], [[1], [], [2, 3]]]:
        print(f"  {mat} -> {flatten(mat)}")

    # Ошибки
    # print("min_max([]):")
    # print(min_max([]))

    # print("flatten([[1, 2], "ab"]):")
    # print(flatten([[1, 2], "ab"]))
    