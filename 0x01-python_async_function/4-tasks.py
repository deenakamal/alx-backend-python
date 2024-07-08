#!/usr/bin/env python3
"""Module"""

import asyncio
from typing import List

task_wait_random = __import__('3-tasks').task_wait_random


async def task_wait_n(n: int, max_delay: int) -> List[float]:
    """Executes task_wait_random"""
    list_waited = []
    for i in range(n):
        wait_time = await task_wait_random(max_delay)
        list_waited.append(wait_time)

    return sorted(list_waited)
