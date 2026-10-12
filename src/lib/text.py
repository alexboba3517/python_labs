"""Функции обработки текста: нормализация, токенизация, частоты слов.

Модуль создан в ЛР3 и переиспользуется в следующих лабораторных работах.
Все функции чистые: не читают ввод, ничего не печатают и не изменяют
переданные им аргументы.
"""

import re

WORD_PATTERN = r"\w+(?:-\w+)*"


def normalize(text: str, *, casefold: bool = True, yo2e: bool = True) -> str:
    r"""Нормализует текст для последующего подсчёта слов.

    Шаги:
      1. Опускает регистр: casefold() при casefold=True, иначе lower().
      2. Если yo2e=True — заменяет «ё» на «е» (заглавная «Ё» к этому
         моменту уже стала строчной после шага 1).
      3. Заменяет любые пробельные символы (\t, \r, \n, неразрывный
         пробел и т.п.) на один пробел и обрезает пробелы по краям.

    Входная строка не изменяется (строки неизменяемы) — возвращается новая.

    Args:
        text: исходный текст.
        casefold: True — casefold() (для сравнения, Unicode-корректно),
            False — lower().
        yo2e: заменять ли «ё» на «е».

    Returns:
        Нормализованная строка.

    Raises:
        TypeError: если text не является строкой.

    Examples:
        >>> normalize("ПрИвЕт\nМИр\t")
        'привет мир'
        >>> normalize("ёжик, Ёлка")
        'ежик, елка'
        >>> normalize("Hello\r\nWorld")
        'hello world'
        >>> normalize("  двойные   пробелы  ")
        'двойные пробелы'
        >>> normalize("Ёжик", yo2e=False)
        'ёжик'
        >>> normalize("Straße")
        'strasse'
        >>> normalize("Straße", casefold=False)
        'straße'
        >>> normalize("")
        ''
        >>> normalize(" \t\n ")
        ''
        >>> normalize(42)
        Traceback (most recent call last):
            ...
        TypeError: normalize: ожидалась строка, получен int
    """
    if not isinstance(text, str):
        raise TypeError(f"normalize: ожидалась строка, получен {type(text).__name__}")
    if casefold:
        text = text.casefold()
    else:
        text = text.lower()
    if yo2e:
        text = text.replace("ё", "е")
    return " ".join(text.split())


def tokenize(text: str) -> list[str]:
    r"""Разбивает текст на слова (токены).

    Словом считается последовательность символов \w (буквы любого
    алфавита, цифры, «_»), в которой допускается дефис внутри слова:
    шаблон \w+(?:-\w+)*. Всё остальное (пробелы, пунктуация, тире «—»,
    эмодзи) — разделители. Регистр и «ё» не трогаются: предполагается,
    что текст уже прошёл normalize().

    Args:
        text: исходный (обычно нормализованный) текст.

    Returns:
        Список слов в порядке появления в тексте, с повторами.

    Raises:
        TypeError: если text не является строкой.

    Examples:
        >>> tokenize("привет мир")
        ['привет', 'мир']
        >>> tokenize("hello,world!!!")
        ['hello', 'world']
        >>> tokenize("по-настоящему круто")
        ['по-настоящему', 'круто']
        >>> tokenize("2025 год")
        ['2025', 'год']
        >>> tokenize("emoji 😀 не слово")
        ['emoji', 'не', 'слово']
        >>> tokenize("-да- a--b")
        ['да', 'a', 'b']
        >>> tokenize("раз—два")
        ['раз', 'два']
        >>> tokenize("")
        []
        >>> tokenize(42)
        Traceback (most recent call last):
            ...
        TypeError: tokenize: ожидалась строка, получен int
    """
    if not isinstance(text, str):
        raise TypeError(f"tokenize: ожидалась строка, получен {type(text).__name__}")
    return re.findall(WORD_PATTERN, text)


def count_freq(tokens: list[str]) -> dict[str, int]:
    """Считает, сколько раз встречается каждое слово.

    Один проход по списку: для каждого токена берётся текущий счёт
    через get(token, 0) (0 — если слово встретилось впервые) и
    увеличивается на 1. Ключи идут в порядке первого появления слова.
    Входной список не изменяется.

    Args:
        tokens: список слов (обычно результат tokenize()).

    Returns:
        Словарь «слово → количество».

    Raises:
        TypeError: если tokens не является списком.

    Examples:
        >>> count_freq(["a", "b", "a", "c", "b", "a"])
        {'a': 3, 'b': 2, 'c': 1}
        >>> count_freq(["bb", "aa", "bb", "aa", "cc"]) == {"aa": 2, "bb": 2, "cc": 1}
        True
        >>> count_freq(["ёж"])
        {'ёж': 1}
        >>> count_freq([])
        {}
        >>> count_freq("abc")
        Traceback (most recent call last):
            ...
        TypeError: count_freq: ожидался список, получен str
    """
    if not isinstance(tokens, list):
        raise TypeError(f"count_freq: ожидался список, получен {type(tokens).__name__}")
    freq: dict[str, int] = {}
    for token in tokens:
        freq[token] = freq.get(token, 0) + 1
    return freq


def top_n(freq: dict[str, int], n: int = 5) -> list[tuple[str, int]]:
    """Возвращает n самых частых слов.

    Пары (слово, частота) сортируются по ключу (-частота, слово):
    минус даёт убывание по частоте, а при равной частоте слова идут
    по алфавиту. reverse=True не используется — он развернул бы и
    алфавитный порядок. Входной словарь не изменяется.

    Args:
        freq: словарь «слово → количество» (обычно результат count_freq()).
        n: сколько пар вернуть; если слов меньше — вернутся все.

    Returns:
        Список кортежей (слово, частота) длиной не больше n.

    Raises:
        TypeError: если freq не словарь или n не целое число.
        ValueError: если n отрицательное.

    Examples:
        >>> top_n({"a": 3, "b": 2, "c": 1}, n=2)
        [('a', 3), ('b', 2)]
        >>> top_n({"bb": 2, "aa": 2, "cc": 1}, n=2)
        [('aa', 2), ('bb', 2)]
        >>> top_n({"x": 1, "y": 5})
        [('y', 5), ('x', 1)]
        >>> top_n({"a": 1}, n=0)
        []
        >>> top_n({})
        []
        >>> top_n({"a": 1}, n=-1)
        Traceback (most recent call last):
            ...
        ValueError: top_n: n не может быть отрицательным, получено -1
        >>> top_n({"a": 1}, n=2.5)
        Traceback (most recent call last):
            ...
        TypeError: top_n: ожидалось целое число, получен float
    """
    if not isinstance(freq, dict):
        raise TypeError(f"top_n: ожидался словарь, получен {type(freq).__name__}")
    if not isinstance(n, int):
        raise TypeError(f"top_n: ожидалось целое число, получен {type(n).__name__}")
    if n < 0:
        raise ValueError(f"top_n: n не может быть отрицательным, получено {n}")
    return sorted(freq.items(), key=lambda p: (-p[1], p[0]))[:n]
