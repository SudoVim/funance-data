import datetime
from typing import Any, Mapping, Optional
import yfinance as yf

from funance_data.store.document import Document
from funance_data.store.store import Store


class TickerInfo(Document):
    """
    Information about a ticker symbol.
    """

    date: datetime.datetime
    symbol: str
    long_name: str
    short_name: str
    dividend_yield: float

    def __init__(self, data: Mapping[str, Any]) -> None:
        super().__init__(data)

        self.date = datetime.datetime.strptime(data["date"], "%Y-%m-%d")
        self.symbol = data["symbol"]

        doc = data.get("doc", {})
        self.dividend_yield = doc.get("yield") or doc.get("dividendYield") or 0.0
        self.long_name = doc.get("longName") or ""
        self.short_name = doc.get("shortName") or ""


class TickerInfoStore(Store[TickerInfo]):
    """
    Store for storing and retrieving information about a ticker symbol.
    """

    symbol: str
    _ticker: yf.Ticker

    def __init__(self, symbol: str) -> None:
        self.symbol = symbol
        self._ticker = yf.Ticker(symbol)

        super().__init__(
            "ticker-info",
            TickerInfo,
            query={
                "bool": {
                    "must": [
                        {
                            "match": {
                                "symbol": {
                                    "query": self.symbol,
                                    "operator": "and",
                                },
                            },
                        },
                    ],
                },
            },
            sort=[
                {
                    "date": {
                        "order": "desc",
                    },
                },
            ],
            index_spec={
                "properties": {
                    "date": {
                        "type": "date",
                    },
                },
            },
        )

    def latest(self) -> Optional[TickerInfo]:
        """
        Get and return the latest ticker info if it exists.
        """
        rsp = self.search(size=1)
        if not rsp.hits:
            return None

        return rsp.hits[0]

    def query(self, force: bool = False) -> TickerInfo:
        """
        Query the ticker information for today if it doesn't exist. ``force``
        overrides this and always queries the latest.
        """
        today = datetime.datetime.utcnow()

        latest = self.latest()
        if latest is not None and not force:
            latest_delta = today - latest.date

            # We already have today's data. Just continue.
            if latest_delta < datetime.timedelta(days=1):
                return latest

        info = self._ticker.info
        date_string = today.strftime("%Y-%m-%d")
        d = TickerInfo.decode(
            {
                "symbol": self.symbol,
                "date": date_string,
                "doc": info,
            }
        )
        self.index(f"{self.symbol}-{date_string}", d)

        return d
