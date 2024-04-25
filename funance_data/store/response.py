from typing import Any, Callable, Generic, Mapping, Optional, TypeVar, get_args

from elastic_transport import ObjectApiResponse

from funance_data.store.document import D


class Response(Generic[D]):
    """
    Base class to be used to interface with different responses to store
    methods.
    """

    data: ObjectApiResponse[Any]

    def __init__(self, data: ObjectApiResponse[Any]) -> None:
        self.data = data


class IndexResponse(Response[D]):
    """
    Response to the :meth:`store.Store.index` method. The type of document will
    match that of the :class:`store.DataStore` itself.
    """


class SearchResponse(Response[D]):
    """
    Response to the :meth:`store.Store.search` method. The type of document will
    match that of the :class:`store.DataStore` itself.

    .. autoattribute:: hits
    """

    _hits: Optional[list[D]]
    _document_class: type[D]

    def __init__(self, data: ObjectApiResponse[Any], document_class: type[D]) -> None:
        super().__init__(data)

        self._hits = None
        self._document_class = document_class

    @property
    def hits(self) -> list[D]:
        """
        the search hits
        """
        if self._hits is not None:
            return self._hits

        self._hits = [
            self._document_class.decode(h)
            for h in self.data.get("hits", {}).get("hits", [])
        ]

        return self._hits
