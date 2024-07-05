#!/usr/bin/env python3
""" Module """
from typing import Callable


def make_multiplier(multiplier: float) -> Callable[[float], float]:
    """Multipy function"""
    def multiply_fun(n: float) -> float:
        """ multiplier with n"""
        return n * multiplier

    return multiply_fun
