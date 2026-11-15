"""Hand-calculated and adversarial daily-v2 cases; no external network."""
import pandas as pd
import pytest

from src.ranking.daily import daily_factors, rank_daily
from src.analytics.screening import shortlist, screening_check
from src.analytics.validation import forward_check


def sample(days=2, size=12):
    return pd.DataFrame([{"symbol": f"S{i:02d}", "index_group": "VN30", "tradingDate": day.date().isoformat(),
                          "openPrice": 100, "closePrice": 100 + i, "totalTradingValue": 1000 * (i + 1),
                          "foreignBuyValue": 100 * i, "foreignSellValue": 100,
                          "foreignBuyVolume": 100, "foreignSellVolume": 100 * i}
                         for day in pd.bdate_range("2026-11-02", periods=days) for i in range(size)])


def test_foreign_balance_is_same_scope_and_zero_is_not_missing():
    row = sample().iloc[0].to_dict()
    row.update(foreignBuyValue=3000, foreignSellValue=1000)
    factors, reason = daily_factors(row)
    assert reason is None and factors["foreign_ratio"] == .5
    assert (factors["foreign_gross"], factors["foreign_net"]) == (4000, 2000)
    # Foreign gross can exceed matched turnover: it includes put-through. No false rejection.
    row.update(foreignBuyValue=0, foreignSellValue=0)
    factors, reason = daily_factors(row)
    assert reason is None and factors["foreign_ratio"] == 0 and factors["foreign_activity"] is False
    row["foreignBuyValue"] = None
    assert daily_factors(row)[0] is None


@pytest.mark.parametrize("bad", [-1, True, float("inf"), float("nan"), "bad"])
def test_invalid_foreign_input_never_scores(bad):
    row = sample().iloc[0].to_dict()
    row["foreignBuyValue"] = bad
    assert daily_factors(row)[0] is None


def test_missing_future_does_not_replace_top_member():
    frame = sample()
    frame.loc[(frame.symbol == "S11") & (frame.tradingDate == "2026-11-03"), "closePrice"] = None
    pair = forward_check(frame, weights=("balanced",))["weights"]["balanced"]["pairs"][0]
    assert pair["top_symbols"] == ["S07", "S08", "S09", "S10", "S11"]
    assert pair["missing_future"] == ["S11"] and pair["evaluated"] == 11 and pair["ranked"] == 12
    assert pair["top_minus_bottom_pp"] is None and "không thay" in pair["spread_reason"]


def test_absent_future_row_does_not_remove_frozen_member():
    frame = sample()
    frame = frame[~((frame.symbol == "S11") & (frame.tradingDate == "2026-11-03"))]
    pair = forward_check(frame, weights=("balanced",))["weights"]["balanced"]["pairs"][0]
    assert "S11" in pair["top_symbols"] and pair["top_minus_bottom_pp"] is None


def test_missing_session_not_silently_bridged_but_supplied_calendar_handles_holiday():
    frame = sample()
    frame.loc[frame.tradingDate == "2026-11-03", "tradingDate"] = "2026-11-04"
    result = forward_check(frame, weights=("balanced",))
    assert result["pairs"] == 0 and len(result["skipped_pairs"]) == 1
    supplied = forward_check(frame, weights=("balanced",), session_dates=["2026-11-02", "2026-11-04"])
    assert supplied["pairs"] == 1 and supplied["calendar"]["mode"] == "supplied"
    with pytest.raises(ValueError, match="bao phủ"):
        forward_check(frame, session_dates=["2026-11-02"])


def test_ties_are_inclusive_and_overlap_has_no_spread():
    scores = pd.Series([100, 90, 80, 70, 60, 60, 10], index=list("ABCDEFG"))
    assert shortlist(scores) == list("ABCDEF")
    assert shortlist(scores.sample(frac=1, random_state=42)) == list("ABCDEF")
    frame = sample()
    for col in ("closePrice", "totalTradingValue", "foreignBuyValue", "foreignSellValue"):
        frame[col] = 100
    pair = forward_check(frame, weights=("balanced",))["weights"]["balanced"]["pairs"][0]
    assert len(pair["top_symbols"]) == len(pair["bottom_symbols"]) == 12
    assert pair["ic"] is None and pair["top_minus_bottom_pp"] is None
    assert "giao nhau" in pair["spread_reason"]


def test_volume_config_changes_rank_and_validation_matches_daily():
    frame = sample()
    value = forward_check(frame, weights=("balanced",), foreign="value")
    volume = forward_check(frame, weights=("balanced",), foreign="volume")
    assert value["foreign"] != volume["foreign"]
    expected = rank_daily(frame[frame.tradingDate == "2026-11-02"].to_dict("records"), foreign="volume").set_index("symbol")
    pair = volume["weights"]["balanced"]["pairs"][0]
    assert pair["config_id"] == expected.config_id.iloc[0]
    assert pair["top_symbols"] == shortlist(expected.total_score)
    assert value["weights"]["balanced"]["factor_ic"]["foreign"]["mean"] == pytest.approx(1)
    assert volume["weights"]["balanced"]["factor_ic"]["foreign"]["mean"] == pytest.approx(-1)


def test_sensitivity_has_common_cohort_and_hand_calculated_missing_top():
    report = screening_check(sample(days=1))
    comparisons = report["details"]
    for row in comparisons:
        if row["kind"] in {"ablation", "single_factor", "weights"}:
            assert row["common_size"] == 12 and row["jaccard"] == 1
    masked = next(r for r in comparisons if r["kind"] == "missing" and r["name"] == "S11")
    assert masked["removed"] == ["S11"] and masked["added"] == ["S06"]
    assert masked["jaccard"] == pytest.approx(4 / 6)
    assert masked["common_top_comparison"]["jaccard"] == 1


def test_missing_one_of_ten_stops_ranking_and_daily_rejects_mixed_dates():
    report = screening_check(sample(days=1, size=10))
    cases = [r for r in report["details"] if r["kind"] == "missing"]
    assert all(r["unranked"] and r["other_size"] == 0 for r in cases)
    with pytest.raises(ValueError):
        rank_daily(sample().to_dict("records"))
