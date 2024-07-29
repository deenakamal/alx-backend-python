#!/usr/bin/env python3
"""Unit tests for the GithubOrgClient class."""
from unittest.mock import patch, Mock, PropertyMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
import unittest
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """Tests the functionality of the GithubOrgClient class."""

    @parameterized.expand(
        [
            ("google"),
            ("abc"),
        ]
    )
    @patch("client.get_json", return_value={"payload": True})
    def test_org(self, org_name: str, mock_get: Mock) -> None:
        """Tests the `org` property of GithubOrgClient.

        Args:
            org_name (str): The name of the GitHub organization.
            mock_get (Mock): Mock object for the `get_json` function.

        Asserts:
            The `org` property returns the expected payload.
            The `get_json` function is called with the correct URL.
        """
        github_org_client = GithubOrgClient(org_name)
        self.assertEqual(github_org_client.org, {"payload": True})
        url = f"https://api.github.com/orgs/{org_name}"
        mock_get.assert_called_once_with(url)

    @patch("client.GithubOrgClient.org", new_callable=PropertyMock)
    def test_public_repos_url(self, mock_org) -> None:
        """Tests the `_public_repos_url` property of GithubOrgClient.

        Args:
            mock_org (PropertyMock): Mock object for the `org` property.

        Asserts:
            The `_public_repos_url` property returns the expected URL.
        """
        payload = {"repos_url": "https://api.github.com/orgs/google/repos"}
        mock_org.return_value = payload
        github_org_client = GithubOrgClient("google")
        self.assertEqual(github_org_client._public_repos_url,
                         payload["repos_url"])

    @patch("client.get_json",
           return_value=[{"name": "repo1"}, {"name": "repo2"}])
    def test_public_repos(self, mock_get_json) -> None:
        """Tests the `public_repos` method of GithubOrgClient.

        Args:
            mock_get_json (Mock): Mock object for the `get_json` function.

        Asserts:
            The `public_repos` method returns the list of repository names.
            The `get_json` and `_public_repos_url` methods are called once.
        """
        with patch(
            "client.GithubOrgClient._public_repos_url",
            new_callable=PropertyMock
        ) as mock_public_repos_url:
            mock_public_repos_url.return_value = (
                "https://api.github.com/orgs/google/repos"
            )
            github_org_client = GithubOrgClient("google")
            self.assertEqual(github_org_client.public_repos(),
                             ["repo1", "repo2"])
            mock_get_json.assert_called_once()
            mock_public_repos_url.assert_called_once()

    @parameterized.expand(
        [
            ({"license": {"key": "my_license"}}, "my_license", True),
            ({"license": {"key": "other_license"}}, "my_license", False),
        ]
    )
    def test_has_license(self, repo, license_key, expected_result) -> None:
        """Tests the `has_license` method of GithubOrgClient.

        Args:
            repo (Dict): The repository data.
            license_key (str): The license key to check for.
            expected_result (bool): The expected result of the license check.

        Asserts:
            The `has_license` method returns the expected result.
        """
        github_org_client = GithubOrgClient("google")
        self.assertEqual(
            github_org_client.has_license(repo, license_key), expected_result
        )


@parameterized_class(('org_payload', 'repos_payload',
                      'expected_repos', 'apache2_repos'), TEST_PAYLOAD)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for the GithubOrgClient class."""

    @classmethod
    def setUpClass(cls):
        """Sets up mock responses for integration tests."""
        cls.get_patcher = patch("requests.get")
        cls.mock_get = cls.get_patcher.start()

        def side_effect(url):
            """Provides mock responses based on the requested URL.

            Args:
                url (str): The URL being requested.

            Returns:
                MockResponse: Mocked response object with JSON data.
            """
            class MockResponse:
                def __init__(self, json_data):
                    self.json_data = json_data

                def json(self):
                    return self.json_data

            if url.endswith("/orgs/google"):
                return MockResponse(cls.org_payload)
            elif url.endswith("/orgs/google/repos"):
                return MockResponse(cls.repos_payload)
            else:
                return None

        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Cleans up the mock patcher after tests."""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Integration test for `public_repos` method with mocked data.

        Asserts:
            The `public_repos` method returns the expected repositories.
        """
        github_org_client = GithubOrgClient("google")
        self.assertEqual(github_org_client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Integration test for `public_repos` method with license filter.
        """
        github_org_client = GithubOrgClient("google")
        self.assertEqual(github_org_client.public_repos(license="apache-2.0"),
                         self.apache2_repos)
