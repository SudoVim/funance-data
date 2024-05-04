from typing import Any, Generic, Generator, Optional
import elasticsearch
import elasticsearch.helpers

from funance_data.client import get_client
from funance_data.config import config
from funance_data.store.document import D
from funance_data.store.response import IndexResponse, SearchResponse


class Store(Generic[D]):
    """
    This ``Store`` class provides a common interface into functionality
    related to accessing data from the underlying elasticsearch store.

    .. autoattribute:: name
    .. autoattribute:: client

    .. automethod:: get_index_name
    .. automethod:: create_index
    .. automethod:: index
    .. automethod:: search
    .. automethod:: stream_update
    """

    #: name of the index representing this data store
    name: str

    #: how to query the configured data store for subclasses of this class
    _query: Optional[dict]

    #: how to sort this data store
    _sort: Optional[list]

    #: spec for indexing this data store
    _index_spec: Optional[dict]

    #: underlying client object to use
    client: elasticsearch.Elasticsearch

    _document_class: type[D]

    def __init__(
        self,
        name: str,
        document_class: type[D],
        query: Optional[dict] = None,
        sort: Optional[list] = None,
        index_spec: Optional[dict] = None,
        client: Optional[elasticsearch.Elasticsearch] = None,
    ):
        self.name = name
        self._document_class = document_class
        self._query = query
        self._sort = sort
        self._index_spec = index_spec
        self.client = client or get_client()

    def get_index_name(self) -> str:
        """
        Get and return the name of this index.
        """
        prefix = config("elasticsearch.index_prefix") or ""

        return f"{prefix}{self.name}"

    def create_index(self) -> None:
        """
        Create the index, optionally with the configured spec.
        """
        index_name = self.get_index_name()
        if not self.client.indices.exists(index=index_name):
            self.client.indices.create(index=index_name)

        if self._index_spec:
            self.client.indices.put_mapping(
                index=index_name,
                body=self._index_spec,
            )

    def index(self, _id: str, document: D) -> IndexResponse[D]:
        """
        Index the given ``document`` at the given ``_id``.
        """
        index_name = self.get_index_name()
        rsp = self.client.index(index=index_name, id=_id, document=document.encode())

        return IndexResponse[D](rsp)

    def search(self, size: int = 10000) -> SearchResponse[D]:
        """
        Search entries
        """
        body = {}  # type: dict[str, Any]

        if self._query:
            body["query"] = self._query

        if self._sort:
            body["sort"] = self._sort

        index_name = self.get_index_name()
        rsp = self.client.search(
            index=index_name,
            body=body,
            size=size,
        )

        return SearchResponse[D](rsp, self._document_class)

    def stream_update(self, update: Generator[tuple[str, D], Any, None]) -> None:
        """
        Stream the given ``update`` to our elasticsearch client.
        """
        index_name = self.get_index_name()

        def bulk_upload():
            for _id, doc in update:
                yield {
                    "_op_type": "update",
                    "_index": index_name,
                    "_id": _id,
                    "doc": doc.encode(),
                    "doc_as_upsert": True,
                }

        for _ in elasticsearch.helpers.streaming_bulk(self.client, bulk_upload()):
            pass
