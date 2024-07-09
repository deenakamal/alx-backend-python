#!/usr/bin/env python3
''' Module '''

import asyncio
from typing import List

async_generator = __import__('0-async_generator').async_generator


async def async_comprehension() -> List[float]:
    '''coroutine will collect 10 random numbers '''
    return [num async for num in async_generator()]
