from unittest.mock import MagicMock, patch

from funance_data.store.test_store.common import StoreTestCase


@patch("funance_data.store.store.config")
class TestGetIndexName(StoreTestCase):
    def test_no_prefix_none(self, mock_config: MagicMock) -> None:
        mock_config.return_value = None
        self.assertEqual("my-store", self.store.get_index_name())
        mock_config.assert_called_once_with("elasticsearch.index_prefix")

    def test_no_prefix_empty(self, mock_config: MagicMock) -> None:
        mock_config.return_value = ""
        self.assertEqual("my-store", self.store.get_index_name())
        mock_config.assert_called_once_with("elasticsearch.index_prefix")

    def test_with_prefix(self, mock_config: MagicMock) -> None:
        mock_config.return_value = "my-prefix-"
        self.assertEqual("my-prefix-my-store", self.store.get_index_name())
        mock_config.assert_called_once_with("elasticsearch.index_prefix")
