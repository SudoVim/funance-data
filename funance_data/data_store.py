from typing import Any, Generic, Optional, TypeVar
from elastic_transport import ObjectApiResponse
import elasticsearch

from funance_data.client import get_client
from funance_data.config import config
from funance_data.document import Document

T = TypeVar("T", bound=Document)


class IndexResponse(Generic[T]):
    response: ObjectApiResponse[Any]

    def __init__(self, response: ObjectApiResponse[Any]) -> None:
        self.response = response


class DataStore(Generic[T]):
    """
    This ``DataStore`` class provides a common interface into functionality
    related to accessing data from the underlying elasticsearch store.

    .. autoattribute:: name
    .. autoattribute:: query
    .. autoattribute:: sort
    .. autoattribute:: index_spec
    .. autoattribute:: client

    .. automethod:: get_index_name
    .. automethod:: create_index
    """

    #: name of the index representing this data store
    name: str

    #: how to query the configured data store for subclasses of this class
    query: Optional[dict]

    #: how to sort this data store
    sort: Optional[list]

    #: spec for indexing this data store
    index_spec: Optional[dict]

    #: underlying client object to use
    client: elasticsearch.Elasticsearch

    def __init__(
        self,
        name: str,
        query: Optional[dict] = None,
        sort: Optional[list] = None,
        index_spec: Optional[dict] = None,
        client: Optional[elasticsearch.Elasticsearch] = None,
    ):
        self.name = name
        self.query = query
        self.sort = sort
        self.index_spec = index_spec
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

        if self.index_spec:
            self.client.indices.put_mapping(
                index=index_name,
                body=self.index_spec,
            )

    def index(self, _id: str, document: T) -> IndexResponse[T]:
        """
        Index the given ``document`` at the given ``_id``.
        """
        index_name = self.get_index_name()
        rsp = self.client.index(index=index_name, id=_id, document=document.encode())

        return IndexResponse[T](rsp)
