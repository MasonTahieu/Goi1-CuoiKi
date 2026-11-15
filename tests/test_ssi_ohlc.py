from datetime import date, datetime, timedelta

import pytest

from src.data.store import TZ
from src.neo_api.rest import NeoError
from src.ssi_api import v3_ohlc


def bar(at, close="29.65", volume="2400"):
    return {"symbol": "GVR", "tradingDate": at, "open": "29.60", "high": "29.80",
            "low": "29.20", "close": close, "volume": volume}


class CandleClient:
    def __init__(self):
        self.calls = []
        self.pages = {
            "1d": [[bar("2026/11/10"), bar("2026/11/09", "29.50")], []],
            "5m": [[bar("2026/11/10 14:45:00"), bar("2026/11/10 14:40:00")],
                   [bar("2026/11/09 14:45:00")]],
        }

    def get(self, route, params):
        assert route == "ohlc" and params["symbol"] == "GVR"
        self.calls.append(params)
        return {"pageSize": 2, "data": self.pages[params["timeFrame"]][params["pageIndex"] - 1]}

    def symbol_summaries(self, symbol, group, start, end):
        assert (symbol, group, start, end) == ("GVR", "VN30", date(2026, 11, 10), date(2026, 11, 10))
        return [{"closePrice": 29650}]


def test_fetch_only_requested_timeframe_and_respect_cutoff():
    client = CandleClient()
    cutoff = datetime(2026, 11, 10, 14, 40, tzinfo=TZ)
    bars = v3_ohlc.chart_candles(client, "GVR", "5m", date(2026, 11, 1), cutoff)
    assert [(call["timeFrame"], call["pageIndex"]) for call in client.calls] == [
        ("5m", 1), ("5m", 2),
    ]
    assert client.calls[0]["from"] == "2026/11/01 00:00:00"
    assert client.calls[0]["to"] == "2026/11/10 23:59:59"
    assert [entry["at"] for entry in bars] == ["2026-11-09T14:45:00+07:00", cutoff.isoformat()]
    assert bars[-1] == {"symbol": "GVR", "timeframe": "5m", "at": cutoff.isoformat(), "open": 29600,
                       "high": 29800, "low": 29200, "price": 29650, "volume": 2400}


def test_bad_intraday_time_does_not_publish_partial_history():
    client = CandleClient()
    client.pages["5m"][0][0]["tradingDate"] = "14:45:00"
    with pytest.raises(NeoError, match="thiếu ngày hoặc giờ"):
        v3_ohlc.chart_candles(client, "GVR", "5m", date(2026, 11, 1), datetime(2026, 11, 10, 15, tzinfo=TZ))


def test_ssi_identical_duplicates_are_counted_once_and_conflicts_are_reported():
    client = CandleClient()
    first = bar("2026/11/10 14:45:00")
    second = bar("2026/11/10 14:40:00")
    client.pages["5m"] = [[first, dict(first)], [dict(first), second], []]
    args = (client, "GVR", "5m", date(2026, 11, 1), date(2026, 11, 10))
    candles = v3_ohlc.fetch_candles(*args)
    assert [candle["at"] for candle in candles] == ["2026-11-10T14:40:00+07:00", "2026-11-10T14:45:00+07:00"]
    assert sum(candle["volume"] for candle in candles) == 4800

    client.pages["5m"][1][0]["volume"] = "2500"
    with pytest.raises(NeoError, match="giá trị khác nhau"):
        v3_ohlc.fetch_candles(*args)


def test_ten_year_query_returns_all_daily_candles_without_intraday_requests():
    end = date(2026, 11, 10)
    first_trade = date(2018, 1, 5)
    windows = []

    class LongHistoryClient(CandleClient):
        def get(self, route, params):
            assert route == "ohlc" and params["pageIndex"] == 1 and params["timeFrame"] == "1d"
            start = datetime.strptime(params["from"], "%Y/%m/%d 00:00:00").date()
            through = datetime.strptime(params["to"], "%Y/%m/%d 23:59:59").date()
            windows.append((start, through))
            if through < first_trade:
                return {}  # The SSI SDK maps an empty HTTP 204 response to an empty dict.
            return {"data": [bar(day.isoformat()) for day in trading_days(max(start, first_trade), through)]}

    def trading_days(start, through):
        for offset in range((through - start).days + 1):
            day = start + timedelta(days=offset)
            if day.weekday() < 5:
                yield day

    start = v3_ohlc.chart_start("1d", "10y", end, end)
    cutoff = datetime(2026, 11, 10, 15, tzinfo=TZ)
    history = v3_ohlc.chart_candles(LongHistoryClient(), "GVR", "1d", start, cutoff)
    assert windows[0][0] == date(2016, 11, 10) and windows[-1][1] == end
    assert all((through - start).days < 365 for start, through in windows)
    assert all(b[0] - a[1] == timedelta(days=1) for a, b in zip(windows, windows[1:]))
    assert len(history) > 2000
    assert [row["at"][:10] for row in history] == [day.isoformat() for day in trading_days(first_trade, end)]


def test_chart_session_reuses_the_same_login(monkeypatch):
    logins = []

    class FakeClient:
        login_mode = None

        def __init__(self, settings):
            assert settings == "test"

        def login(self, mode):
            logins.append(mode)
            self.login_mode = mode

    monkeypatch.setattr(v3_ohlc, "_client", None)
    monkeypatch.setattr(v3_ohlc, "load_ssi_settings", lambda: "test")
    monkeypatch.setattr(v3_ohlc, "V3Client", FakeClient)
    assert v3_ohlc.chart_client() is v3_ohlc.chart_client()
    assert logins == ["none"]
