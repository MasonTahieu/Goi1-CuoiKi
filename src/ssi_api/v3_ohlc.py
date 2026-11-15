"""Historical SSI candles for charting, fetched through the existing read-only V3 client."""
from datetime import datetime, time, timedelta
from math import isclose
from threading import Lock

from src.data.store import TZ
from src.neo_api.rest import NeoError
from src.ssi_api.settings import load_ssi_settings
from src.ssi_api.v3_client import MAX_PAGES, SYMBOL, V3Client, _number, parse_day
from src.ssi_api.v3_decoder import source_time


PAGE_SIZE = 500
REQUEST_DAYS = {"1d": 365, "5m": 31}
PRICE_FIELDS = ("open", "high", "low", "price")
CHART_RANGES = {
    "1d": {"5": 15, "10": 28, "30": 75, "60": 150, "1y": 1, "5y": 5, "10y": 10},
    "5m": {"30": 10, "100": 10, "1m": 31, "1y": 1},
}
DEFAULT_RANGE = {"1d": "1y", "5m": "100"}
_client_lock = Lock()
_client = None


def chart_client():
    """Reuse the market-data session for chart requests in this server process."""
    global _client
    with _client_lock:
        if _client is None:
            client = V3Client(load_ssi_settings())
            try:
                client.login("none")
            except NeoError:
                client.close()
                raise
            _client = client
        elif _client.login_mode is None:
            _client.login("none")
        return _client


def _years_before(day, years):
    year = day.year - years
    try:
        return day.replace(year=year)
    except ValueError:
        return day.replace(year=year, day=28)  # Leap day in a non-leap target year.


def chart_start(timeframe, window, end, today):
    size = CHART_RANGES[timeframe][window]
    start = _years_before(end, size) if window.endswith("y") else end - timedelta(days=size - 1)
    return max(start, _years_before(today, 1)) if timeframe == "5m" else start


def _bar(raw, symbol, timeframe, start, end):
    if not isinstance(raw, dict) or str(raw.get("symbol", "")).upper() != symbol:
        raise NeoError("SSI OHLC trả về bản ghi sai mã.")
    value = raw.get("tradingDate")
    if timeframe == "1d":
        at = datetime.combine(parse_day(value), time(15), tzinfo=TZ)
    else:
        at, issue = source_time(value, datetime.combine(end, time.min, tzinfo=TZ))
        if at is None or issue or at.time() == time.min:
            raise NeoError("Nến 5 phút thiếu ngày hoặc giờ nguồn hợp lệ.")
    if not start <= at.date() <= end:
        raise NeoError("SSI OHLC trả về nến ngoài khoảng ngày yêu cầu.")
    invalid = []
    prices = {field: _number(raw.get("close" if field == "price" else field), field, invalid)
              for field in PRICE_FIELDS}
    volume = _number(raw.get("volume"), "volume", invalid)
    if (invalid or any(price is None or price <= 0 for price in prices.values())
            or not prices["low"] <= min(prices["open"], prices["price"])
            or not prices["high"] >= max(prices["open"], prices["price"])
            or volume is not None and volume < 0):
        raise NeoError("SSI OHLC trả về giá hoặc khối lượng nến không hợp lệ.")
    return {"symbol": symbol, "timeframe": timeframe, "at": at.isoformat(), **prices, "volume": volume}


def fetch_candles(client, symbol, timeframe, start, end):
    if not SYMBOL.fullmatch(symbol) or timeframe not in CHART_RANGES or start > end:
        raise NeoError("Mã, khung nến hoặc khoảng ngày SSI OHLC không hợp lệ.")
    result = {}
    # The live OHLC API requires a time component for daily bars too (SSI 400213).
    since = start.strftime("%Y/%m/%d 00:00:00")
    until = end.strftime("%Y/%m/%d 23:59:59")
    for page in range(1, MAX_PAGES + 1):
        body = client.get("ohlc", {
            "symbol": symbol, "timeFrame": timeframe,
            "from": since, "to": until,
            "pageIndex": page, "pageSize": PAGE_SIZE,
        })
        if isinstance(body, dict) and (not body or str(body.get("code")) == "204"):
            break
        rows = body.get("data") if isinstance(body, dict) else None
        if not isinstance(rows, list):
            raise NeoError("SSI OHLC trả về dữ liệu sai cấu trúc.")
        for raw in rows:
            bar = _bar(raw, symbol, timeframe, start, end)
            previous = result.setdefault(bar["at"], bar)
            if previous != bar:
                raise NeoError("SSI OHLC trả các giá trị khác nhau cho cùng một mốc nến.")
        size = body.get("pageSize")
        size = size if type(size) is int and size > 0 else PAGE_SIZE
        if len(rows) < size:
            break
    else:
        raise NeoError("Khoảng nến vượt giới hạn phân trang. Hãy chọn khoảng ngày ngắn hơn.")
    return sorted(result.values(), key=lambda bar: bar["at"])


def _price_scale(price, reference):
    for scale in (1, 1000):
        if isclose(price * scale, reference, rel_tol=0.12):
            return scale
    raise NeoError("Đơn vị giá SSI OHLC chưa khớp giá SSI cùng phiên.")


def chart_candles(client, symbol, timeframe, start, cutoff):
    """Read just the selected chart from SSI and return the candles in memory."""
    end = cutoff.date()
    days = (end - start).days + 1
    width = REQUEST_DAYS[timeframe]
    candles = []
    for offset in range(0, days, width):
        since = start + timedelta(days=offset)
        through = since + timedelta(days=min(width, days - offset) - 1)
        candles.extend(fetch_candles(client, symbol, timeframe, since, through))
    candles = [bar for bar in candles if bar["at"] <= cutoff.isoformat()]
    if not candles:
        return []
    anchor = candles[-1]
    anchor_day = parse_day(anchor["at"])
    summaries = client.symbol_summaries(symbol, "VN30", anchor_day, anchor_day)
    reference = summaries[0].get("closePrice") if summaries else None
    if not reference or reference <= 0:
        raise NeoError("Chưa có giá cuối ngày SSI để đối chiếu đơn vị nến.")
    scale = _price_scale(anchor["price"], reference)
    for bar in candles:
        for field in PRICE_FIELDS:
            bar[field] *= scale
    return candles
