"""Next-session check (src.analytics.validation). Offline, synthetic daily rows."""
import pandas as pd
import pytest

from src.analytics.validation import adjustment_note, forward_check, verdict, write_evidence


def rows(days=4, size=12, momentum=lambda i, d: 0.2 * i, close_change=lambda i, d: 0.0):
    """Higher i -> higher turnover and foreign ratio. ``momentum`` sets open-to-close of each day."""
    out = []
    for d in range(days):
        for i in range(size):
            out.append({"symbol": f"S{i:02d}", "index_group": "VN30", "tradingDate": pd.bdate_range("2026-11-02", periods=days)[d].date().isoformat(),
                        "openPrice": 10_000, "closePrice": 10_000 * (1 + momentum(i, d) / 100),
                        "totalTradingValue": 1e9 * (i + 1), "foreignBuyValue": 1e7 * i, "foreignSellValue": 1e7,
                        "priceChangePercent": close_change(i, d)})
    out.append({"symbol": "VN30", "index_group": "INDEX", "tradingDate": "2026-11-01", "closePrice": 1800.0})
    return pd.DataFrame(out)


def test_ordering_kept_next_session_gives_ic_one_and_positive_spread():
    result = forward_check(rows())
    part = result["weights"]["balanced"]
    assert result["sessions"] == 4 and result["pairs"] == 3
    assert [p["ic"] for p in part["pairs"]] == pytest.approx([1, 1, 1])
    assert part["ic"]["mean"] == pytest.approx(1) and part["ic"]["positive_share"] == 1
    assert part["top_minus_bottom_pp"]["mean"] == pytest.approx(0.2 * 7)  # mean(7..11) - mean(0..4)
    assert all(p["ranked"] == 12 for p in part["pairs"])


def test_reversed_ordering_is_reported_as_negative_not_hidden():
    flips = lambda i, d: 0.2 * i if d % 2 == 0 else -0.2 * i
    part = forward_check(rows(days=2, momentum=flips))["weights"]["balanced"]
    assert part["ic"]["mean"] == pytest.approx(-1)


def test_return_comes_from_the_next_session_only():
    # Same-day open-to-close matches the score perfectly, the next day is the reverse: a look-ahead
    # bug (using same-day returns) would report +1, the correct check reports -1.
    result = forward_check(rows(days=2, momentum=lambda i, d: 0.2 * i if d == 0 else -0.2 * i))
    assert result["weights"]["balanced"]["pairs"][0]["ic"] == pytest.approx(-1)


def test_tradable_return_is_separate_from_the_close_to_close_figure():
    # Next session moves up from the close for the high scorers, then falls back after the open:
    # counting from the close looks good, what could actually be bought does not.
    frame = rows(days=2, momentum=lambda i, d: 0.2 * i if d == 0 else -0.2 * i, close_change=lambda i, d: 0.1 * i)
    part = forward_check(frame)["weights"]["balanced"]
    assert part["pairs"][0]["ic"] == pytest.approx(-1)
    assert part["pairs"][0]["ic_close"] == pytest.approx(1)
    assert part["ic_close"]["pairs"] == part["top_minus_bottom_close_pp"]["pairs"] == 1


def test_adjustment_note_follows_the_data(tmp_path):
    frame = rows(days=3, momentum=lambda i, d: 0.0, close_change=lambda i, d: 0.0)
    clean = forward_check(frame)["adjustment"]
    assert clean["flagged"] == [] and clean["compared"] == 24 and clean["ref_price_present"] == 0
    assert "chưa được kiểm chứng" in adjustment_note(clean)
    frame.loc[(frame["symbol"] == "S03") & (frame["tradingDate"] == "2026-11-03"), "priceChangePercent"] = 4.0
    flagged = forward_check(frame)["adjustment"]
    assert flagged["flagged"] == [{"symbol": "S03", "tradingDate": "2026-11-03"}]
    assert "S03 2026-11-03" in adjustment_note(flagged) and "chưa được kiểm chứng" not in adjustment_note(flagged)


def test_verdict_is_descriptive_even_for_extreme_ic_and_evidence_reproduces(tmp_path):
    import json
    import hashlib
    flat = forward_check(rows(momentum=lambda i, d: 0.2 * i if d == 0 else 0.0))["weights"]["balanced"]
    assert flat["ic"]["pairs"] == 0 and verdict(flat) == "Chưa đủ phiên để kiểm tra."
    strong = {"ic": {"pairs": 9, "mean": 1.0, "sd": 0.0, "positive_share": 1}}
    assert "chưa xác lập" in verdict(strong)
    frame = rows()
    result = forward_check(frame)
    assert "power" not in result["weights"]["balanced"]
    assert "t" not in result["weights"]["balanced"]["ic"]
    write_evidence(result, tmp_path, frame)
    text = (tmp_path / "KIEM_TRA_PHIEN_KE_TIEP.md").read_text(encoding="utf-8")
    assert "Lợi suất mở cửa–đóng cửa" in text and "+1,000" in text and "Điều chỉnh quyền" in text
    payload = (tmp_path / "input_daily.json").read_bytes()
    manifest = json.loads((tmp_path / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["input_sha256"] == hashlib.sha256(payload).hexdigest()
    assert forward_check(pd.DataFrame(json.loads(payload))) == result
    assert len(pd.read_csv(tmp_path / "kiem_tra_phien_ke_tiep.csv")) == 6


def test_unranked_rows_and_index_rows_are_excluded():
    frame = rows()
    frame.loc[frame["symbol"].isin(["S00", "S01"]), "foreignBuyValue"] = None  # missing foreign -> unranked
    part = forward_check(frame)["weights"]["balanced"]
    assert all(p["ranked"] == 10 for p in part["pairs"])
    assert part["ic"]["mean"] == pytest.approx(1)
