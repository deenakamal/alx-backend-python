#!/usr/bin/env python3
"""Unit tests for utility functions.
This module contains unit tests for the following utility functions:
- `access_nested_map`: Accesses a nested map using a path of keys.
- `get_json`: Fetches JSON data from a URL.
- `memoize`: Caches the result of a method call to optimize performance.
"""
import unittest
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize
from typing import Any, Tuple, Dict
from unittest.mock import patch, Mock


class TestAccessNestedMap(unittest.TestCase):
    """Tests for the `access_nested_map` function."""

    @parameterized.expand(
        [
            ({"a": 1}, ("a",), 1),
            ({"a": {"b": 2}}, ("a",), {"b": 2}),
            ({"a": {"b": 2}}, ("a", "b"), 2),
        ]
    )
    def test_access_nested_map(
        self, nested_map: Dict[str, Any], path: Tuple[str], expected: Any
    ) -> None:
        """Tests `access_nested_map` with various inputs.

        Args:
            nested_map (Dict[str, Any]): The nested dictionary to search.
            path (Tuple[str]): The path of keys to access.
            expected (Any): The expected value at the end of the path.

        Asserts:
            The result of `access_nested_map` matches the expected value.
        """
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([({}, ("a",)), ({"a": 1}, ("a", "b"))])
    def test_access_nested_map_exception(
        self, nested_map: Dict[str, Any], path: Tuple[str]
    ) -> None:
        """Tests `access_nested_map` for cases where a KeyError is expected.

        Args:
            nested_map (Dict[str, Any]): The nested dictionary to search.
            path (Tuple[str]): The path of keys to access.

        Asserts:
            `access_nested_map` raises a KeyError for invalid paths.
        """
        with self.assertRaises(KeyError):
            access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    """Tests for the `get_json` function.

    The `get_json` function fetches JSON data from a given URL.
    """

    @parameterized.expand(
        [
            ("http://example.com", {"payload": True}),
            ("http://holberton.io", {"payload": False}),
        ]
    )
    @patch("requests.get")
    def test_get_json(
        self, test_url: str, test_payload: Dict[str, Any], mock_get: Mock
    ) -> None:
        """Tests `get_json` with various URLs and payloads.

        Args:
            test_url (str): The URL to fetch JSON from.
            test_payload (Dict[str, Any]): The expected JSON payload.
            mock_get (Mock): Mock object for `requests.get`.

        Asserts:
            The result of `get_json` matches the expected payload.
            `requests.get` is called once with the correct URL.
        """
        mock_get.return_value.json.return_value = test_payload
        self.assertEqual(get_json(test_url), test_payload)
        mock_get.assert_called_once_with(test_url)


class TestMemoize(unittest.TestCase):
    """Tests for the `memoize` decorator.

    """

    def test_memoize(self) -> None:
        """Tests the `memoize` decorator."""

        class TestClass:
            """A test class to demonstrate the `memoize` decorator."""

            def a_method(self) -> int:
                """Returns a fixed integer value.

                Returns:
                    int: The value 42.
                """
                return 42

            @memoize
            def a_property(self) -> int:
                """Returns the result of `a_method`.

                Returns:
                    int: The result of `a_method`.
                """
                return self.a_method()

        with patch.object(TestClass, "a_method", return_value=42) as mocked:
            test_class = TestClass()
            self.assertEqual(test_class.a_property, 42)
            self.assertEqual(test_class.a_property, 42)
            mocked.assert_called_once()
