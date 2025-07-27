#!/usr/bin/env python3
"""Unit tests for GithubOrgClient class."""

import unittest
from parameterized import parameterized
from unittest.mock import patch, PropertyMock
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Tests for various methods in GithubOrgClient."""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """Test that .org calls get_json with correct URL and returns payload."""
        expected_payload = {"payload": True}
        mock_get_json.return_value = expected_payload

        client = GithubOrgClient(org_name)
        result = client.org

        expected_url = f"https://api.github.com/orgs/{org_name}"
        mock_get_json.assert_called_once_with(expected_url)
        self.assertEqual(result, expected_payload)

    def test_public_repos_url(self):
        """Test that _public_repos_url returns repos_url from mocked org payload."""
        expected_url = "https://api.github.com/orgs/google/repos"

        with patch.object(
            GithubOrgClient,
            'org',
            new_callable=PropertyMock
        ) as mock_org:
            mock_org.return_value = {"repos_url": expected_url}

            client = GithubOrgClient("google")
            self.assertEqual(client._public_repos_url, expected_url)
            mock_org.assert_called_once()

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test that public_repos returns repo names and calls mocks once."""
        mock_get_json.return_value = [
            {"name": "repo1"},
            {"name": "repo2"},
        ]

        with patch.object(
            GithubOrgClient,
            '_public_repos_url',
            new_callable=PropertyMock
        ) as mock_repos_url:
            mock_repos_url.return_value = "https://fakeurl.com/orgs/google/repos"

            client = GithubOrgClient("google")
            result = client.public_repos()

            self.assertEqual(result, ["repo1", "repo2"])
            mock_get_json.assert_called_once_with(
                "https://fakeurl.com/orgs/google/repos"
            )
            mock_repos_url.assert_called_once()

    @patch('client.get_json')
    def test_public_repos_with_license(self, mock_get_json):
        """Test that public_repos filters repos by license key correctly."""
        mock_get_json.return_value = [
            {"name": "repo1", "license": {"key": "apache-2.0"}},
            {"name": "repo2", "license": {"key": "other"}},
        ]

        with patch.object(
            GithubOrgClient,
            '_public_repos_url',
            new_callable=PropertyMock
        ) as mock_repos_url:
            mock_repos_url.return_value = "https://fakeurl.com/orgs/google/repos"

            client = GithubOrgClient("google")
            result = client.public_repos(license="apache-2.0")

            self.assertEqual(result, ["repo1"])
            mock_get_json.assert_called_once_with(
                "https://fakeurl.com/orgs/google/repos"
            )
            mock_repos_url.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test has_license returns correct boolean based on repo license key."""
        self.assertEqual(
            GithubOrgClient.has_license(repo, license_key),
            expected
        )
