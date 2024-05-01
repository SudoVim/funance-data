import unittest
from unittest.mock import MagicMock

from funance_data.store.document import Document
from funance_data.store.response import SearchResponse


class DocumentSubClass(Document):
    pass


class TestSearchResponse(unittest.TestCase):
    def test_hits_already_defined(self) -> None:
        data = MagicMock()
        rsp = SearchResponse[DocumentSubClass](data, DocumentSubClass)
        rsp._hits = []

        cmp_hits = rsp.hits

        self.assertEqual([], cmp_hits)
        data.get.assert_not_called()

    def test_hits_no_hits(self) -> None:
        data = MagicMock()
        data.get.return_value = {}

        rsp = SearchResponse[DocumentSubClass](data, DocumentSubClass)

        cmp_hits = rsp.hits

        self.assertEqual([], cmp_hits)
        data.get.assert_called_once_with("hits", {})

    def test_hits_empty_hits(self) -> None:
        data = MagicMock()
        data.get.return_value = {"hits": []}

        rsp = SearchResponse[DocumentSubClass](data, DocumentSubClass)

        cmp_hits = rsp.hits

        self.assertEqual([], cmp_hits)
        data.get.assert_called_once_with("hits", {})

    def test_hits_no_source(self) -> None:
        data = MagicMock()
        data.get.return_value = {"hits": [{"my-key": "my-val"}]}

        rsp = SearchResponse[DocumentSubClass](data, DocumentSubClass)

        cmp_hits = rsp.hits

        self.assertEqual(1, len(cmp_hits))
        cmp_hit = cmp_hits[0]
        self.assertEqual(DocumentSubClass, type(cmp_hit))
        self.assertEqual({}, cmp_hit.data)

        data.get.assert_called_once_with("hits", {})

    def test_hits(self) -> None:
        data = MagicMock()
        data.get.return_value = {"hits": [{"_source": {"my-key": "my-val"}}]}

        rsp = SearchResponse[DocumentSubClass](data, DocumentSubClass)

        cmp_hits = rsp.hits

        self.assertEqual(1, len(cmp_hits))
        cmp_hit = cmp_hits[0]
        self.assertEqual(DocumentSubClass, type(cmp_hit))
        self.assertEqual({"my-key": "my-val"}, cmp_hit.data)

        data.get.assert_called_once_with("hits", {})
