#!/usr/bin/env python3

""" Module to sum a list of mixed integers and floats. """

from typing import List, Union


def sum_mixed_list(mxd_lst: List[Union[int, float]]) -> float:
    """ Return the sum of a mixed list of floats and integers. """
    return float(sum(mxd_lst))
