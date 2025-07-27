#!/usr/bin/env python3
"""Unit tests for GithubOrgClient.org method."""

import unittest
from parameterized import parameterized
from unittest.mock import patch, PropertyMock
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


class TestGithubOrgClient(unittest.TestCase):
    """Tests for GithubOrgClient"""

    def test_public_repos_url(self):
        """Test that _public_repos_url returns expected URL from mocked org payload."""
        expected_url = "https://api.github.com/orgs/google/repos"

        # Patch GithubOrgClient.org (a memoized property)
        with patch.object(GithubOrgClient, 'org', new_callable=PropertyMock) as mock_org:
            mock_org.return_value = {"repos_url": expected_url}

            client = GithubOrgClient("google")
            self.assertEqual(client._public_repos_url, expected_url)
            mock_org.assert_called_once()
            

@patch('client.get_json')
def test_public_repos(self, mock_get_json):
    """Test that public_repos returns expected repo list and calls mocks once."""
    # Fake payload returned by get_json
    mock_get_json.return_value = [
        {"name": "repo1"},
        {"name": "repo2"},
    ]

    # Patch _public_repos_url property
    with patch.object(GithubOrgClient, '_public_repos_url', new_callable=PropertyMock) as mock_repos_url:
        mock_repos_url.return_value = "https://fakeurl.com/orgs/google/repos"

        client = GithubOrgClient("google")
        result = client.public_repos()

        # Assert repo names are correct
        self.assertEqual(result, ["repo1", "repo2"])

        # Assert mocks were called once
        mock_get_json.assert_called_once_with("https://fakeurl.com/orgs/google/repos")
        mock_repos_url.assert_called_once()


class TestGithubOrgClient(unittest.TestCase):
    # ... previous tests ...

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test has_license returns correct boolean based on repo license key."""
        self.assertEqual(GithubOrgClient.has_license(repo, license_key), expected)
