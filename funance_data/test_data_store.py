import unittest
from unittest.mock import MagicMock, patch

from funance_data.data_store import DataStore


class DataStoreTest(unittest.TestCase):
    mock_client: MagicMock
    store: DataStore

    def setUp(self) -> None:
        super().setUp()

        self.mock_client = MagicMock()
        self.store = DataStore("my-store", client=self.mock_client)

    def test_get_index_name_no_prefix(self):
        self.assertEqual("my-store", self.store.get_index_name())

    @patch("funance_data.data_store.config")
    def test_get_index_name_with_prefix(self, mock_config: MagicMock):
        mock_config.return_value = "my-prefix-"
        self.assertEqual("my-prefix-my-store", self.store.get_index_name())

        mock_config.assert_called_once_with("elasticsearch.index_prefix")

    def test_create_index_does_not_exist(self):
        self.mock_client.indices.exists.return_value = False

        self.store.create_index()

        self.mock_client.indices.exists.assert_called_once_with(index="my-store")
        self.mock_client.indices.create.assert_called_once_with(index="my-store")
        self.mock_client.indices.put_mapping.assert_not_called()

    def test_create_index_exists(self):
        self.mock_client.indices.exists.return_value = True

        self.store.create_index()

        self.mock_client.indices.exists.assert_called_once_with(index="my-store")
        self.mock_client.indices.create.assert_not_called()
        self.mock_client.indices.put_mapping.assert_not_called()

    def test_create_index_with_spec(self):
        self.store.index_spec = {"some": "spec"}

        self.store.create_index()

        self.mock_client.indices.put_mapping.assert_called_once_with(
            index="my-store",
            body={"some": "spec"},
        )
