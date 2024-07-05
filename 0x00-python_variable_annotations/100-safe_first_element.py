#!/usr/bin/env python3
""" Module """
from typing import Sequence, Any, Union


def safe_first_element(lst: Sequence[Any]) -> Union[Any, None]:
    """
    Return the first element of lst if it is not empty,
    otherwise return None.

    Args:
        lst (Sequence[Any]): A sequence of elements of any type.
    """

    if lst:
        return lst[0]
    else:
        return None
