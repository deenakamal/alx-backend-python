#!/usr/bin/env python3
"""Unit tests for utility functions.
This module contains unit tests for the following utility functions:
- `access_nested_map`: Accesses a nested map using a path of keys."""

import unittest
from utils import access_nested_map, get_json
from parameterized import parameterized
from unittest.mock import patch, Mock

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
    def test_access_nested_map_exception(self, nested_map, path):
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
        
    
    
    class TestGetJson(unittest.TestCase):
        """
        Test case for the get_json function in utils.py.
        Ensures it calls requests.get and returns the correct JSON payload
        without performing a real HTTP request.
        """
        @parameterized.expand([
            ("http://example.com", {"payload": True}),
            ("http://holberton.io", {"payload": False}),
        ])
        @patch('utils.requests.get')
        def test_get_json(self, test_url, test_payload, mock_get):
            """ Create a mock responde with .json() returnin test_playload."""
            mock_response = Mock() # create mock object for response
            mock_response.json.return_value = test_payload #ser .json() return value
            mock_get.return_value = mock_response # request.get() return this mock
            
            result = get_json(test_url)
            mock_get.assert_called_once_with(test_url)
            self.assertEqual(result, test_payload)  