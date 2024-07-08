#!/usr/bin/env python3
""" Module """
import random
import asyncio


async def wait_random(max_delay: int = 10) -> float:
    """ wait the time that get from random and excusess the function"""
    random_value = random.uniform(0, max_delay)
    await asyncio.sleep(random_value)

    return random_value
