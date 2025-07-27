#!/usr/bin/env python3
"""Unit tests for utility functions.
This module contains unit tests for the following utility functions:
- `access_nested_map`: Accesses a nested map using a path of keys."""

import unittest
from utils import access_nested_map
from parameterized import parameterized

class TestAccessNestedMap(unittest.TestCase):
    """Create a TestAccessNestedMap class that inherits from unittest.TestCase"""
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path , expected):
        """Test Case"""
        self.assertEqual(access_nested_map(nested_map, path), expected)
        
    
    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),   
    ])
    def test_access_nested_map_except(self, nested_map, path):
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
        # Ensure the error message matches the first missing key
        self.assertEqual(str(context.exception), repr(path[-1]))
        
        