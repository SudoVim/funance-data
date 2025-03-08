from unittest.mock import MagicMock, patch
from funance_data.store.document import Document
from funance_data.store.test_store.common import StoreTestCase


class TestStreamUpdate(StoreTestCase):
    @patch("elasticsearch.helpers")
    def test_no_data(self, mock_helpers: MagicMock) -> None:
        self.store.stream_update([].__iter__())  # type: ignore

        mock_helpers.streaming_bulk.assert_called()
        cmp_client, cmp_bulk_upload = mock_helpers.streaming_bulk.mock_calls[0].args
        self.assertEqual(self.mock_client, cmp_client)
        self.assertEqual([], list(cmp_bulk_upload))

    @patch("elasticsearch.helpers")
    def test_with_data(self, mock_helpers: MagicMock) -> None:
        self.store.stream_update(
            [
                ("my-id", Document.decode({"my-key": "my-val"})),
            ].__iter__()  # type: ignore
        )

        mock_helpers.streaming_bulk.assert_called()
        cmp_client, cmp_bulk_upload = mock_helpers.streaming_bulk.mock_calls[0].args
        self.assertEqual(self.mock_client, cmp_client)
        self.assertEqual(
            [
                {
                    "_id": "my-id",
                    "_index": self.store.get_index_name(),
                    "_op_type": "update",
                    "doc": {"my-key": "my-val"},
                    "doc_as_upsert": True,
                }
            ],
            list(cmp_bulk_upload),
        )
