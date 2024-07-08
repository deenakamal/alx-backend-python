#!/usr/bin/env python3
""" Module """

from typing import List

wait_random = __import__('0-basic_async_syntax').wait_random


async def wait_n(n: int, max_delay: int) -> List[float]:
    """
    Return the list of all the delays (float values)
    in ascending order
    """
    list_waited = []
    for i in range(n):
        wait_time = await wait_random(max_delay)
        list_waited.append(wait_time)

    return sorted(list_waited)
