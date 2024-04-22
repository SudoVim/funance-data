import unittest
from unittest.mock import MagicMock, patch, call

import elasticsearch

from funance_data.client import create_new_client, get_client, app_local


@patch("elasticsearch.Elasticsearch")
class TestCreateNewClient(unittest.TestCase):
    def test(self, mock_elasticsearch: MagicMock) -> None:
        cmp_client = create_new_client("my-host", "my-user", "my-pass")
        self.assertIsNotNone(cmp_client)

        mock_elasticsearch.assert_called_once_with(
            ["my-host"], http_auth=("my-user", "my-pass")
        )


@patch("funance_data.client.config")
@patch("funance_data.client.create_new_client")
class TestGetClient(unittest.TestCase):
    def tearDown(self) -> None:
        app_local.__delattr__("global_elastic_client")

    def test_create(
        self, mock_create_new_client: MagicMock, mock_config: MagicMock
    ) -> None:
        mock_config.side_effect = [
            "my-host",
            "my-user",
            "my-pass",
        ]

        cmp_client = get_client()
        self.assertIsNotNone(cmp_client)

        mock_create_new_client.assert_called_once_with("my-host", "my-user", "my-pass")
        mock_config.assert_has_calls(
            [
                call("elasticsearch.url"),
                call("elasticsearch.username"),
                call("elasticsearch.password"),
            ]
        )

    def test_already_created(
        self, mock_create_new_client: MagicMock, mock_config: MagicMock
    ) -> None:
        app_local.global_elastic_client = MagicMock(spec=elasticsearch.Elasticsearch)

        cmp_client = get_client()
        self.assertIsNotNone(cmp_client)

        mock_create_new_client.assert_not_called()
        mock_config.assert_not_called()
