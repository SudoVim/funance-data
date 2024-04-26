from funance_data.store.test_store.common import StoreTestCase


class TestCreateIndex(StoreTestCase):
    def test_does_not_exist(self) -> None:
        self.mock_client.indices.exists.return_value = False
        self.store.create_index()
        self.mock_client.indices.exists.assert_called_once_with(index="my-store")
        self.mock_client.indices.create.assert_called_once_with(index="my-store")
        self.mock_client.indices.put_mapping.assert_not_called()

    def test_exists(self) -> None:
        self.mock_client.indices.exists.return_value = True
        self.store.create_index()
        self.mock_client.indices.exists.assert_called_once_with(index="my-store")
        self.mock_client.indices.create.assert_not_called()
        self.mock_client.indices.put_mapping.assert_not_called()

    def test_with_spec(self) -> None:
        self.store.index_spec = {"my": "spec"}
        self.mock_client.indices.exists.return_value = True
        self.store.create_index()
        self.mock_client.indices.exists.assert_called_once_with(index="my-store")
        self.mock_client.indices.create.assert_not_called()
        self.mock_client.indices.put_mapping.assert_called_once_with(
            index="my-store", body={"my": "spec"}
        )
