import datetime
from unittest import TestCase
from unittest.mock import MagicMock, patch

from yfinance import Ticker

from funance_data.tickers.info import TickerInfo, TickerInfoStore


class TestTickerInfo(TestCase):
    def test_decode(self) -> None:
        info = TickerInfo.decode(
            {
                "date": "2024-04-28",
                "symbol": "AAPL",
            }
        )
        self.assertEqual("Sun Apr 28 00:00:00 2024", info.date.strftime("%c"))
        self.assertEqual("AAPL", info.symbol)


class TestTickerInfoStore(TestCase):
    mock_client: MagicMock
    mock_ticker: MagicMock
    store: TickerInfoStore
    today: datetime.date
    yesterday: datetime.date

    def setUp(self) -> None:
        super().setUp()

        self.mock_client = MagicMock()
        self.mock_ticker = MagicMock(spec=Ticker)
        self.store = TickerInfoStore("AAPL")
        self.store.client = self.mock_client
        self.store._ticker = self.mock_ticker

        self.today = datetime.date(2024, 4, 30)
        self.yesterday = datetime.date(2024, 4, 29)

    def test_init(self) -> None:
        self.assertEqual(
            {
                "bool": {
                    "must": [
                        {
                            "match": {
                                "symbol": {
                                    "query": "AAPL",
                                    "operator": "and",
                                },
                            },
                        },
                    ],
                },
            },
            self.store._query,
        )

    def test_latest_not_found(self) -> None:
        self.mock_client.search.return_value = {"hits": {"hits": []}}
        cmp_doc = self.store.latest()
        self.assertIsNone(cmp_doc)
        self.mock_client.search.assert_called_once_with(
            index="ticker-info",
            body={
                "query": {
                    "bool": {
                        "must": [
                            {
                                "match": {
                                    "symbol": {
                                        "query": "AAPL",
                                        "operator": "and",
                                    },
                                },
                            },
                        ],
                    },
                },
                "sort": [{"date": {"order": "desc"}}],
            },
            size=1,
        )

    def test_latest_found(self) -> None:
        self.mock_client.search.return_value = {
            "hits": {
                "hits": [
                    {
                        "_source": {
                            "date": "2024-04-28",
                            "symbol": "AAPL",
                        },
                    },
                ]
            }
        }
        cmp_doc = self.store.latest()
        assert cmp_doc is not None

        self.assertEqual(TickerInfo, type(cmp_doc))
        self.mock_client.search.assert_called_once_with(
            index="ticker-info",
            body={
                "query": {
                    "bool": {
                        "must": [
                            {
                                "match": {
                                    "symbol": {
                                        "query": "AAPL",
                                        "operator": "and",
                                    },
                                },
                            },
                        ],
                    },
                },
                "sort": [{"date": {"order": "desc"}}],
            },
            size=1,
        )
        self.assertEqual(
            {
                "date": "2024-04-28",
                "symbol": "AAPL",
            },
            cmp_doc.encode(),
        )

    @patch("funance_data.tickers.info.datetime.date")
    def test_query_latest_found(self, mock_date: MagicMock) -> None:
        mock_date.today.return_value = self.today
        mock_date.strptime.return_value = self.today
        self.mock_client.search.return_value = {
            "hits": {
                "hits": [
                    {
                        "_source": {
                            "date": "2024-04-30",
                            "symbol": "AAPL",
                        },
                    },
                ]
            }
        }
        cmp_doc = self.store.query()
        self.assertIsNotNone(cmp_doc)
        self.assertEqual(TickerInfo, type(cmp_doc))

        mock_date.today.assert_called_once_with()

        self.assertEqual(
            {
                "date": "2024-04-30",
                "symbol": "AAPL",
            },
            cmp_doc.encode(),
        )
        self.mock_client.index.assert_not_called()

    @patch("funance_data.tickers.info.datetime.date")
    def test_query_latest_found_outdated(self, mock_date: MagicMock) -> None:
        mock_date.today.return_value = self.today
        mock_date.strptime.return_value = self.yesterday
        self.mock_client.search.return_value = {
            "hits": {
                "hits": [
                    {
                        "_source": {
                            "date": "2024-04-29",
                            "symbol": "AAPL",
                        },
                    },
                ]
            }
        }
        cmp_doc = self.store.query()
        self.assertIsNotNone(cmp_doc)
        self.assertEqual(TickerInfo, type(cmp_doc))

        mock_date.today.assert_called_once_with()

        self.assertEqual(
            {
                "date": "2024-04-30",
                "symbol": "AAPL",
                "doc": self.mock_ticker.info,
            },
            cmp_doc.encode(),
        )
        self.mock_client.index.assert_called_once_with(
            index="ticker-info",
            id="AAPL-2024-04-30",
            document={
                "symbol": "AAPL",
                "date": "2024-04-30",
                "doc": self.mock_ticker.info,
            },
        )

    @patch("funance_data.tickers.info.datetime.date")
    def test_query_latest_not_found(self, mock_date: MagicMock) -> None:
        mock_date.today.return_value = self.today
        self.mock_client.search.return_value = {"hits": {"hits": []}}
        cmp_doc = self.store.query()
        self.assertIsNotNone(cmp_doc)
        self.assertEqual(TickerInfo, type(cmp_doc))

        mock_date.today.assert_called_once_with()

        self.assertEqual(
            {
                "date": "2024-04-30",
                "symbol": "AAPL",
                "doc": self.mock_ticker.info,
            },
            cmp_doc.encode(),
        )
        self.mock_client.index.assert_called_once_with(
            index="ticker-info",
            id="AAPL-2024-04-30",
            document={
                "symbol": "AAPL",
                "date": "2024-04-30",
                "doc": self.mock_ticker.info,
            },
        )
