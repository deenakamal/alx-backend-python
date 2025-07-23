#!/usr/bin/env python3
"""nit tests for utility functions.
This module contains unit tests for the following utility functions:
- `access_nested_map`: Accesses a nested map using a path of keys."""

import unittest
from utils import access_nested_map
from parameterized import parameterized


class TestacessNestedMap(unittest.TestCase):
    """Create a TestAccessNestedMap class that inherits from unittest.TestCase"""
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    
    def test_access_nested_map(self, nested_map, path , expected):
        """ Test Case """
        self.assertEqual(access_nested_map(nested_map, path), expected)