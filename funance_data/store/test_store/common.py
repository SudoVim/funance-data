from unittest import TestCase
from unittest.mock import MagicMock

from funance_data.store.document import Document
from funance_data.store.store import Store


class StoreTestCase(TestCase):
    store: Store
    mock_client: MagicMock

    def setUp(self) -> None:
        super().setUp()

        self.mock_client = MagicMock()
        self.store = Store[Document]("my-store", Document, client=self.mock_client)
