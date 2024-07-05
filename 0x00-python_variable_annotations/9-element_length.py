#!/usr/bin/env python3
""" Module """
from typing import Iterable, Sequence, List, Tuple


def element_length(lst: Iterable[Sequence]) -> List[Tuple[Sequence, int]]:
    """
    Returns a list of tuples where each tuple contains
    an element from lst and its length.

    Args:
        lst (Iterable[Sequence]): An iterable containing sequences
        (like lists, tuples, strings, etc.).

    Returns:
        List[Tuple[Sequence, int]]:
        A list of tuples where each tuple contains an element
        from lst and its length.
    """
    return [(i, len(i)) for i in lst]
