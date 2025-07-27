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
        """Create a mock response with .json() returning test_payload."""
        # Step 1: Create mock response object
        mock_response = Mock()
        mock_response.json.return_value = test_payload
        mock_get.return_value = mock_response

        # Step 2: Call function under test
        result = get_json(test_url)

        # Step 3: Verify requests.get was called correctly
        mock_get.assert_called_once_with(test_url)

        # Step 4: Verify return value is as expected
        self.assertEqual(result, test_payload)