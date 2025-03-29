import datetime
from typing import Any, Generator, Mapping

import yfinance
import dateparser
from funance_data.store.document import Document
from funance_data.store.store import Store


class TickerDaily(Document):
    """
    Daily price data for a ticker.
    """

    date: datetime.datetime
    symbol: str

    open: float
    high: float
    low: float
    close: float

    def __init__(self, data: Mapping[str, Any]) -> None:
        super().__init__(data)

        parsed_date = dateparser.parse(str(data["date"]))
        assert parsed_date is not None

        self.date = parsed_date
        self.symbol = data["symbol"]

        doc = data.get("doc", {})
        self.open = doc.get("Open", 0.0)
        self.high = doc.get("High", 0.0)
        self.low = doc.get("Low", 0.0)
        self.close = doc.get("Close", 0.0)


class TickerDailyStore(Store[TickerDaily]):
    """
    Store for storing and retrieving daily price data for a ticker symbol.
    """

    symbol: str
    _ticker: yfinance.Ticker

    NAME = "ticker-daily"
    SORT = [
        {
            "date": {
                "order": "desc",
            },
        },
    ]
    INDEX_SPEC = {
        "properties": {
            "date": {
                "type": "date",
            },
        },
    }

    def __init__(self, symbol: str) -> None:
        self.symbol = symbol
        self._ticker = yfinance.Ticker(symbol)

        super().__init__(
            TickerDaily,
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
        )

    def query(self, force: bool = False) -> None:
        """
        query the daily ohlc data
        """
        today = datetime.datetime.now()
        from_date = today - datetime.timedelta(days=365 * 10)

        latest = self.latest()
        if latest is not None and not force:
            # Always update the latest date in case there's newer data that we
            # did not get.
            from_date = latest.date

        df = self._ticker.history(start=from_date, end=today)

        def bulk_upload(dates, data) -> Generator[tuple[str, TickerDaily], Any, None]:
            for date, row in zip(dates, data):
                entry = {c: e for c, e in zip(df.columns, row)}
                yield (
                    f"{self.symbol}-{date}",
                    TickerDaily.decode(
                        {
                            "symbol": self.symbol,
                            "date": date,
                            "doc": entry,
                        }
                    ),
                )

        self.stream_update(bulk_upload(df.index, df.values))

    def latest(self):
        """
        the latest ohlc datapoint
        """
        rsp = self.search(size=1)
        if not rsp.hits:
            return None

        return rsp.hits[0]
