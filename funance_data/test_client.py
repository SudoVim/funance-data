import unittest
from unittest.mock import MagicMock, patch

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


@patch("os.getenv")
@patch("funance_data.client.create_new_client")
class TestGetClient(unittest.TestCase):
    def tearDown(self) -> None:
        app_local.__delattr__("global_elastic_client")

    def test_default(
        self, mock_create_new_client: MagicMock, mock_getenv: MagicMock
    ) -> None:
        mock_getenv.return_value = ""

        cmp_client = get_client()
        self.assertIsNotNone(cmp_client)

        mock_create_new_client.assert_called_once_with(
            "http://localhost:9200", "elastic", ""
        )

    def test_with_configured(
        self, mock_create_new_client: MagicMock, mock_getenv: MagicMock
    ) -> None:
        env = {
            "ELASTICSEARCH_URL": "my-host",
            "ELASTICSEARCH_USERNAME": "my-user",
            "ELASTICSEARCH_PASSWORD": "my-pass",
        }
        mock_getenv.side_effect = env.get

        cmp_client = get_client()
        self.assertIsNotNone(cmp_client)

        mock_create_new_client.assert_called_once_with("my-host", "my-user", "my-pass")

    def test_already_created(
        self, mock_create_new_client: MagicMock, mock_getenv: MagicMock
    ) -> None:
        app_local.global_elastic_client = MagicMock(spec=elasticsearch.Elasticsearch)

        cmp_client = get_client()
        self.assertIsNotNone(cmp_client)

        mock_create_new_client.assert_not_called()
        mock_getenv.assert_not_called()
