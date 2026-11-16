"""Cached checks must be identical to fresh checks and never survive changed inputs."""
import json

import pytest

from src.data.daily_store import DailyStore, read_daily
from src.web import validation_cache as cache


@pytest.fixture
def dataset(tmp_path):
    rows = [{"symbol": f"S{i:02d}", "index_group": "VN30", "tradingDate": day,
             "openPrice": 10_000, "closePrice": 10_000 + (i - 4) * (d + 1) * 20,
             "totalTradingValue": 1e9 * (i + 1), "priceChangePercent": i * .1,
             "foreignBuyValue": 1e6 * i, "foreignSellValue": 5e6,
             "foreignBuyVolume": 100 * (12 - i), "foreignSellVolume": 500}
            for d, day in enumerate(("2026-11-05", "2026-11-06")) for i in range(12)]
    database = tmp_path / "daily.sqlite"
    with DailyStore(database) as store:
        store.upsert("ssi", rows, "2026-11-06T16:00:00+07:00")
    cache._memory.clear()
    yield database, read_daily(database), tmp_path / "validation.json"
    cache._memory.clear()


def test_bundle_matches_fresh_checks_for_all_four_configurations(dataset, monkeypatch):
    database, frame, path = dataset
    bundle = cache.build_bundle(database, path)
    expected = {}
    for foreign in cache.daily_rank.FOREIGN:
        result = cache.forward_check(frame, foreign=foreign)
        for weights in cache.daily_rank.WEIGHTS:
            expected[weights, foreign] = cache.web_payload(result, weights, foreign)
    assert len(bundle["results"]) == 4
    def no_calculation(*args, **kwargs):
        pytest.fail("A valid precomputed bundle must not recalculate")
    monkeypatch.setattr(cache, "forward_check", no_calculation)
    for (weights, foreign), payload in expected.items():
        assert cache.cached_validation(frame, weights, foreign, path) == payload
    # Callers cannot mutate the process cache through the returned object.
    result = cache.cached_validation(frame, "balanced", "value", path)
    result["summary"].clear()
    assert cache.cached_validation(frame, "balanced", "value", path) == expected["balanced", "value"]


@pytest.mark.parametrize("change", ["data", "code", "corrupt", "missing", "payload"])
def test_changed_or_unusable_bundle_recalculates_and_then_reuses_memory(dataset, monkeypatch, change):
    database, frame, path = dataset
    bundle = cache.build_bundle(database, path)
    if change == "data":
        frame.loc[0, "foreignBuyValue"] = 9e9
    elif change == "code":
        original_signature = cache.signature
        monkeypatch.setattr(cache, "signature", lambda frame: {**original_signature(frame), "code_sha256": "new-code"})
    elif change == "corrupt":
        path.write_text("{", encoding="utf-8")
    elif change == "missing":
        path = path.with_name("absent.json")
    else:
        bundle["results"]["balanced:value"]["payload"]["summary"]["ic"]["mean"] = 12345
        path.write_text(json.dumps(bundle), encoding="utf-8")
    original = cache.forward_check
    calls = []
    def calculate(*args, **kwargs):
        calls.append(1)
        return original(*args, **kwargs)
    monkeypatch.setattr(cache, "forward_check", calculate)
    expected = cache.web_payload(original(frame, weights=("balanced",), foreign="value"), "balanced", "value")
    for _ in range(2):
        assert cache.cached_validation(frame, "balanced", "value", path) == expected
    assert len(calls) == 1


def test_memory_cache_changes_with_data_and_foreign_choice(dataset, monkeypatch):
    _, frame, path = dataset
    calls = []
    original = cache.forward_check
    def calculate(*args, **kwargs):
        calls.append(kwargs["foreign"])
        return original(*args, **kwargs)
    monkeypatch.setattr(cache, "forward_check", calculate)
    cache.cached_validation(frame, "balanced", "value", path)
    cache.cached_validation(frame, "balanced", "volume", path)
    frame.loc[0, "closePrice"] = 12000
    cache.cached_validation(frame, "balanced", "value", path)
    assert calls == ["value", "volume", "value"]
