#!/usr/bin/env python3
"""Unit tests for GithubOrgClient.org method."""

import unittest
from parameterized import parameterized
from unittest.mock import patch
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Tests for the GithubOrgClient.org property."""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns correct value and calls get_json."""
        # Arrange: mock return value
        expected_payload = {"payload": True}
        mock_get_json.return_value = expected_payload

        # Act: instantiate client and access org property
        client = GithubOrgClient(org_name)
        result = client.org

        # Assert: get_json was called once with correct URL
        expected_url = f"https://api.github.com/orgs/{org_name}"
        mock_get_json.assert_called_once_with(expected_url)

        # Assert: result matches mock return
        self.assertEqual(result, expected_payload)
