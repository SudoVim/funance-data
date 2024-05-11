from typing import Type
from unittest import TestCase
from unittest.mock import MagicMock

from funance_data.store.document import Document
from funance_data.store.store import Store


class StoreTestCase(TestCase):
    store_class: Type[Store]
    store: Store
    mock_client: MagicMock

    def setUp(self) -> None:
        super().setUp()

        class TestStore(Store[Document]):

            NAME = "my-store"

        self.store_class = TestStore
        self.mock_client = MagicMock()
        self.store = self.store_class(Document, client=self.mock_client)
