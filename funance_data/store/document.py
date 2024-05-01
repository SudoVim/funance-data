from typing import Any, Mapping, TypeVar
from typing_extensions import Self


class Document:
    """
    Base class for all objects that are meant to be used with
    :class:`DataStore`.

    .. autoattribute:: data
    .. autoattribute:: source

    .. automethod:: encode
    .. automethod:: decode
    """

    #: The raw underlying data
    data: Mapping[str, Any]

    def __init__(self, data: Mapping[str, Any]) -> None:
        self.data = data

    def encode(self) -> Mapping[str, Any]:
        """
        Encode the data in this document to be stored in elasticsearch.
        """
        return self.data

    @classmethod
    def decode(cls, data: Mapping[str, Any]) -> Self:
        """
        Decode the given ``data`` into this document.
        """
        return cls(data)


D = TypeVar("D", bound=Document)
