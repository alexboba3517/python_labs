def is_jagged(mat: list[list[float | int]]) -> bool:
    """Проверяет, является ли матрица рваной (т.е. строки имеют разную длину).

    Args:
        mat: матрица (список списков).

    Returns:
        True, если матрица рваная, иначе False.
        Для пустой матрицы возвращает False.
    """
    if not mat:
        return False
    first_row_len = len(mat[0])
    for row in mat:
        if len(row) != first_row_len:
            return True
    return False


def transpose(mat: list[list[float | int]]) -> list[list]:
    """Возвращает транспонированную матрицу.

    Args:
        mat: матрица (список списков).

    Returns:
        Транспонированная матрица (список списков).

    Raises:
        ValueError: если матрица рваная.

    Examples:
        >>> transpose([[1, 2, 3]])
        [[1], [2], [3]]
        >>> transpose([[1], [2], [3]])
        [[1, 2, 3]]
        >>> transpose([[1, 2], [3, 4]])
        [[1, 3], [2, 4]]
        >>> transpose([])
        []
        >>> transpose([[1, 2], [3]])
        Traceback (most recent call last):
            ...
        ValueError: transpose: матрица рваная
    """

    if is_jagged(mat):
        raise ValueError("transpose: матрица рваная")
    if not mat:
        return []
    transposed = []
    for j in range(len(mat[0])):
        new_row = []
        for i in range(len(mat)):
            new_row.append(mat[i][j])
        transposed.append(new_row)
    return transposed


def row_sums(mat: list[list[float | int]]) -> list[float]:
    """Возвращает сумму строк матрицы.

    Args:
        mat: матрица (список списков).

    Returns:
        Суммы строк матрицы (список чисел).

    Raises:
        ValueError: если матрица пустая или рваная.

    Examples:
        >>> row_sums([[1, 2, 3], [4, 5, 6]])
        [6, 15]
        >>> row_sums([[-1, 1], [10, -10]])
        [0, 0]
        >>> row_sums([[0, 0], [0, 0]])
        [0, 0]
        >>> row_sums([[1, 2], [3]])
        Traceback (most recent call last):
            ...
        ValueError: row_sums: матрица рваная
        >>> row_sums([])
        Traceback (most recent call last):
            ...
        ValueError: row_sums: матрица пустая
    """
    if not mat:
        raise ValueError("row_sums: матрица пустая")
    if is_jagged(mat):
        raise ValueError("row_sums: матрица рваная")
    row_sum = []
    for row in mat:
        row_sum.append(sum(row))
    return row_sum


def col_sums(mat: list[list[float | int]]) -> list[float]:
    """Возвращает сумму столбцов матрицы.

    Args:
        mat: матрица (список списков).

    Returns:
        Суммы столбцов матрицы (список чисел).

    Raises:
        ValueError: если матрица пустая или рваная.


    Examples:
        >>> col_sums([[1, 2, 3], [4, 5, 6]])
        [5, 7, 9]
        >>> col_sums([[-1, 1], [10, -10]])
        [9, -9]
        >>> col_sums([[0, 0], [0, 0]])
        [0, 0]
        >>> col_sums([[1, 2], [3]])
        Traceback (most recent call last):
            ...
        ValueError: col_sums: матрица рваная
        >>> col_sums([])
        Traceback (most recent call last):
            ...
        ValueError: col_sums: матрица пустая
    """
    if not mat:
        raise ValueError("col_sums: матрица пустая")
    if is_jagged(mat):
        raise ValueError("col_sums: матрица рваная")
    sums = []
    for j in range(len(mat[0])):
        col_sum = 0
        for i in range(len(mat)):
            col_sum += mat[i][j]
        sums.append(col_sum)
    return sums


if __name__ == "__main__":
    print("transpose:")
    for mat in [[[1, 2, 3]], [[1], [2], [3]], [[1, 2], [3, 4]], []]:
        print(f"  {mat} -> {transpose(mat)}")

    print("row_sums:")
    for mat in [[[1, 2, 3], [4, 5, 6]], [[-1, 1], [10, -10]], [[0, 0], [0, 0]]]:
        print(f"  {mat} -> {row_sums(mat)}")

    print("col_sums:")
    for mat in [[[1, 2, 3], [4, 5, 6]], [[-1, 1], [10, -10]], [[0, 0], [0, 0]]]:
        print(f"  {mat} -> {col_sums(mat)}")

    # Ошибки:
    # print("transpose([[1, 2], [3]]):")
    # print(transpose([[1, 2], [3]]))

    # print("row_sums([[1, 2], [3]]):")
    # print(row_sums([[1, 2], [3]]))

    # print("col_sums([[1, 2], [3]]):")
    # print(col_sums([[1, 2], [3]]))
