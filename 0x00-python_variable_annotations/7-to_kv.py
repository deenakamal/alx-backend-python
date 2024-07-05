#!/usr/bin/env python3
"""Module"""
from typing import Union, Tuple


def to_kv(k: str, v: Union[int, float]) -> Tuple[str, float]:
    """
    Takes a string k and an int or float v and returns a tuple.
    The first element of the tuple is the string k.
    The second element is the square of the int/float v.

    Args:
        k (str): The string key.
        v (Union[int, float]): The integer or float value.

    Returns:
        Tuple[str, float]: A tuple where the first element is k
        and the second element is v squared as float.
    """
    return (k, float(v ** 2))
