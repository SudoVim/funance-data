import unittest
from unittest.mock import MagicMock, patch

from funance_data.data_store import DataStore, IndexResponse
from funance_data.document import Document


class DataStoreTest(unittest.TestCase):
    mock_client: MagicMock
    store: DataStore

    def setUp(self) -> None:
        super().setUp()

        self.mock_client = MagicMock()
        self.store = DataStore[Document]("my-store", client=self.mock_client)

    def test_get_index_name_no_prefix(self) -> None:
        self.assertEqual("my-store", self.store.get_index_name())

    @patch("funance_data.data_store.config")
    def test_get_index_name_with_prefix(self, mock_config: MagicMock) -> None:
        mock_config.return_value = "my-prefix-"
        self.assertEqual("my-prefix-my-store", self.store.get_index_name())

        mock_config.assert_called_once_with("elasticsearch.index_prefix")

    def test_create_index_does_not_exist(self) -> None:
        self.mock_client.indices.exists.return_value = False

        self.store.create_index()

        self.mock_client.indices.exists.assert_called_once_with(index="my-store")
        self.mock_client.indices.create.assert_called_once_with(index="my-store")
        self.mock_client.indices.put_mapping.assert_not_called()

    def test_create_index_exists(self) -> None:
        self.mock_client.indices.exists.return_value = True

        self.store.create_index()

        self.mock_client.indices.exists.assert_called_once_with(index="my-store")
        self.mock_client.indices.create.assert_not_called()
        self.mock_client.indices.put_mapping.assert_not_called()

    def test_create_index_with_spec(self) -> None:
        self.store.index_spec = {"some": "spec"}

        self.store.create_index()

        self.mock_client.indices.put_mapping.assert_called_once_with(
            index="my-store",
            body={"some": "spec"},
        )

    def test_index(self) -> None:
        doc = Document({"my-key": "my-val"})

        cmp_rsp = self.store.index("my-id", doc)

        self.mock_client.index.assert_called_once_with(
            index="my-store",
            id="my-id",
            document={"my-key": "my-val"},
        )

        self.assertEqual(IndexResponse, type(cmp_rsp))
        self.assertEqual(self.mock_client.index.return_value, cmp_rsp.response)
