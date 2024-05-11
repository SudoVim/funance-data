from funance_data.store.document import Document
from funance_data.store.response import SearchResponse
from funance_data.store.test_store.common import StoreTestCase


class TestSearch(StoreTestCase):
    def test_no_args(self) -> None:
        cmp_rsp = self.store.search()
        self.assertEqual(SearchResponse, type(cmp_rsp))
        self.assertEqual(self.mock_client.search.return_value, cmp_rsp.data)
        self.assertEqual(Document, cmp_rsp._document_class)
        self.mock_client.search.assert_called_once_with(
            index="my-store",
            body={},
            size=10000,
        )

    def test_size(self) -> None:
        cmp_rsp = self.store.search(size=10)
        self.assertEqual(SearchResponse, type(cmp_rsp))
        self.assertEqual(self.mock_client.search.return_value, cmp_rsp.data)
        self.assertEqual(Document, cmp_rsp._document_class)
        self.mock_client.search.assert_called_once_with(
            index="my-store",
            body={},
            size=10,
        )

    def test_query(self) -> None:
        self.store._query = {"my": "query"}
        cmp_rsp = self.store.search()
        self.assertEqual(SearchResponse, type(cmp_rsp))
        self.assertEqual(self.mock_client.search.return_value, cmp_rsp.data)
        self.assertEqual(Document, cmp_rsp._document_class)
        self.mock_client.search.assert_called_once_with(
            index="my-store",
            body={
                "query": {"my": "query"},
            },
            size=10000,
        )

    def test_sort(self) -> None:
        self.store_class.SORT = [{"my": "sort"}]
        cmp_rsp = self.store.search()
        self.assertEqual(SearchResponse, type(cmp_rsp))
        self.assertEqual(self.mock_client.search.return_value, cmp_rsp.data)
        self.assertEqual(Document, cmp_rsp._document_class)
        self.mock_client.search.assert_called_once_with(
            index="my-store",
            body={
                "sort": [{"my": "sort"}],
            },
            size=10000,
        )
