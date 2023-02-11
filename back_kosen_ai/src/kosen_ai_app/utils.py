from typing import List, Any, Callable


def search(l: List[Any], func: Callable[[Any], bool]) -> int:
    """リスト中で条件式に一致する最初の要素のindexを返す

    Args:
        l (List[Any]): 探索するリスト
        func (Callable[[Any], bool]): 条件式

    Raises:
        ValueError: 一致する要素がなければ送出

    Returns:
        int: 条件式に一致したindex
    """
    for i, e in enumerate(l):
        if func(e):
            return i

    raise ValueError("couldn't find element matches the given condition")
