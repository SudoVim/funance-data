from funance_data.store.document import Document
from funance_data.store.response import IndexResponse
from funance_data.store.test_store.common import StoreTestCase


class TestIndex(StoreTestCase):
    def test(self) -> None:
        d = Document.decode({"_source": {"my-key": "my-val"}})
        cmp_rsp = self.store.index("my-id", d)
        self.assertEqual(IndexResponse, type(cmp_rsp))
        self.assertEqual(self.mock_client.index.return_value, cmp_rsp.data)
        self.mock_client.index.assert_called_once_with(
            index="my-store",
            id="my-id",
            document={"_source": {"my-key": "my-val"}},
        )
