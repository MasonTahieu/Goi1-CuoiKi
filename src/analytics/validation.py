"""Retrospective daily-v2 screening sensitivity and descriptive next-session returns.
No significance verdict, power estimate or claim of executable trading returns.
"""
import math
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

from src.ranking.daily import METHOD, WEIGHTS, rank_daily, _num
from src.analytics.screening import shortlist, screening_check

FACTOR_COLUMNS = {"momentum": "momentum", "liquidity": "turnover", "foreign": "foreign_ratio"}
TOP_N = 5
RETURN_LABELS = {"tradable": "lợi suất mở cửa–đóng cửa phiên kế tiếp (mô tả, chưa tính chi phí hay khả năng thực thi)",
                 "close": "priceChangePercent của phiên kế tiếp do SSI cung cấp; chưa xác nhận điều chỉnh quyền"}


def _stats(values):
    values = [v for v in values if v is not None and math.isfinite(v)]
    n = len(values)
    if n == 0:
        return {"pairs": 0, "mean": None, "sd": None, "positive_share": None}
    mean = float(np.mean(values))
    sd = float(np.std(values, ddof=1)) if n > 1 else None
    return {"pairs": n, "mean": mean, "sd": sd, "positive_share": float(np.mean([v > 0 for v in values]))}


def _spearman(a, b):
    if len(a) < 3 or a.nunique() < 2 or b.nunique() < 2:
        return None
    return float(a.rank().corr(b.rank()))


def _spread(joined, column, top, bottom):
    if not top or not bottom or set(top) & set(bottom):
        return None, "Top/Bottom trống hoặc giao nhau do đồng điểm"
    if joined.loc[top + bottom, column].isna().any():
        return None, "Thiếu lợi suất của thành viên đã chốt; không thay mã khác"
    return float(joined.loc[top, column].mean() - joined.loc[bottom, column].mean()), None


def _session_pairs(days, session_dates=None):
    """An explicit calendar may bridge holidays. Default never bridges missing weekdays.

    The fallback is intentionally conservative: it skips a real holiday gap rather than
    silently calling a multi-session return a next-session return. It is not an exchange calendar.
    """
    pairs, skipped = [], []
    calendar = sorted(set(session_dates)) if session_dates is not None else None
    if calendar is not None:
        if any(day not in calendar for day in days):
            raise ValueError("Lịch phiên không bao phủ mọi ngày dữ liệu.")
        next_date = dict(zip(calendar, calendar[1:]))
    for today, nxt in zip(days, days[1:]):
        expected = next_date.get(today) if calendar is not None else (pd.Timestamp(today) + pd.offsets.BDay()).date().isoformat()
        weekday_ok = calendar is not None or pd.Timestamp(today).day_of_week < 5
        if nxt == expected and weekday_ok:
            pairs.append((today, nxt))
        else:
            skipped.append({"date": today, "observed_next": nxt, "expected_next": expected,
                            "reason": "Thiếu phiên hoặc chưa xác nhận lịch nghỉ; không nối qua khoảng trống"})
    return pairs, skipped


def adjustment_check(data, tolerance_pp=0.3):
    """How far SSI's priceChangePercent departs from plain close-to-close: large gaps mark possible ex-rights days."""
    ordered = data.sort_values(["symbol", "tradingDate"])
    plain = 100 * (ordered["closePrice"] / ordered.groupby("symbol")["closePrice"].shift(1) - 1)
    gap = (ordered["priceChangePercent"] - plain).abs().dropna()
    flagged = ordered.loc[gap[gap > tolerance_pp].index, ["symbol", "tradingDate"]].to_dict("records")
    ref = pd.to_numeric(data["refPrice"], errors="coerce") if "refPrice" in data else pd.Series(dtype=float)
    return {"tolerance_pp": tolerance_pp, "compared": int(len(gap)), "flagged": flagged, "ref_price_present": int(ref.notna().sum())}


def forward_check(frame, group="VN30", weights=tuple(WEIGHTS), top_n=TOP_N, foreign="value", session_dates=None):
    """frame: daily summary rows (read_daily). Returns per-pair results and summaries per weight set."""
    data = frame[frame["index_group"] == group].copy()
    for column in ("openPrice", "closePrice", "priceChangePercent"):
        data[column] = pd.to_numeric(data[column].map(_num), errors="coerce") if column in data else float("nan")
        data[column] = data[column].where(np.isfinite(data[column]))
    tradable = 100 * (data["closePrice"] / data["openPrice"].where(data["openPrice"] > 0) - 1)
    data["tradable_return"] = tradable.where(data["closePrice"] > 0)
    days = sorted(data["tradingDate"].unique())
    pairs, skipped = _session_pairs(days, session_dates)
    out = {"method": "next-session-descriptive-v3", "ranking_method": METHOD, "foreign": foreign,
           "group": group, "sessions": len(days), "date_from": days[0] if days else None, "date_to": days[-1] if days else None,
           "pairs": len(pairs), "skipped_pairs": skipped, "top_n": top_n, "returns": RETURN_LABELS,
           "calendar": {"mode": "supplied" if session_dates is not None else "conservative-weekday-guard",
                        "session_dates": sorted(set(session_dates)) if session_dates is not None else None,
                        "note": "Chỉ nối hai ngày liền phiên theo lịch cung cấp, hoặc liền ngày làm việc khi chưa có lịch sở giao dịch; khoảng nghỉ chưa xác nhận bị bỏ."},
           "adjustment": adjustment_check(data), "weights": {}}
    for name in weights:
        rows, factor_ic = [], {f: [] for f in FACTOR_COLUMNS}
        for today, nxt in pairs:
            ranked = rank_daily(data[data["tradingDate"] == today].to_dict("records"), weights=name, foreign=foreign)
            ranked = ranked.drop(columns=["tradable_return", "priceChangePercent"], errors="ignore").set_index("symbol")
            ranked = ranked.dropna(subset=["total_score"])
            top = shortlist(ranked["total_score"], top_n)
            bottom = shortlist(ranked["total_score"], top_n, largest=False)
            future = data[data["tradingDate"] == nxt].set_index("symbol")[["tradable_return", "priceChangePercent"]]
            joined = ranked.join(future, how="left", validate="one_to_one")
            scored = joined.dropna(subset=["total_score", "tradable_return"])
            against_close = joined.dropna(subset=["total_score", "priceChangePercent"])
            for factor, column in FACTOR_COLUMNS.items():
                part = scored if column in scored else scored.iloc[0:0]
                factor_ic[factor].append(_spearman(part[column], part["tradable_return"]) if len(part) else None)
            spread, spread_reason = _spread(joined, "tradable_return", top, bottom)
            spread_close, close_reason = _spread(joined, "priceChangePercent", top, bottom)
            rows.append({"date": today, "next_date": nxt, "ranked": len(ranked), "evaluated": len(scored),
                         "missing_future": sorted(joined.index[joined["tradable_return"].isna()].tolist()),
                         "top_symbols": top, "bottom_symbols": bottom,
                         "config_id": ranked["config_id"].iloc[0] if len(ranked) else None,
                         "spread_reason": spread_reason, "spread_close_reason": close_reason,
                         "ic": _spearman(scored["total_score"], scored["tradable_return"]),
                         "top_minus_bottom_pp": spread,
                         "ic_close": _spearman(against_close["total_score"], against_close["priceChangePercent"]),
                         "top_minus_bottom_close_pp": spread_close})
        ic = _stats([r["ic"] for r in rows])
        out["weights"][name] = {"pairs": rows, "ic": ic,
                                "top_minus_bottom_pp": _stats([r["top_minus_bottom_pp"] for r in rows]),
                                "ic_close": _stats([r["ic_close"] for r in rows]),
                                "top_minus_bottom_close_pp": _stats([r["top_minus_bottom_close_pp"] for r in rows]),
                                "factor_ic": {f: _stats(v) for f, v in factor_ic.items()},
                                "screening": screening_check(data, group, name, foreign, top_n)}
    return out


def _fmt(value, digits=3, sign=True):
    if value is None:
        return "—"
    text = f"{value:+.{digits}f}" if sign else f"{value:.{digits}f}"
    return text.replace(".", ",").replace("-", "−")


def verdict(summary):
    """One honest sentence for the report and the page."""
    ic = summary["ic"]
    if not ic["pairs"]:
        return "Chưa đủ phiên để kiểm tra."
    return (f"Mô tả {ic['pairs']} cặp phiên: IC trung bình {_fmt(ic['mean'])}. "
            "Kết quả chưa xác lập khả năng dự báo hay hiệu quả đầu tư. Điểm giúp ưu tiên danh sách theo dõi; "
            "độ ổn định của danh sách không chứng minh lợi nhuận.")


def adjustment_note(info):
    ref = "`refPrice` trống ở mọi dòng" if not info["ref_price_present"] else f"`refPrice` có ở {info['ref_price_present']} dòng"
    limit = _fmt(info["tolerance_pp"], 1, sign=False)
    if not info["flagged"]:
        return (f"- **Điều chỉnh quyền:** {ref} và trong {info['compared']} dòng so sánh chưa có dòng nào `priceChangePercent` lệch quá "
                f"{limit} điểm % so với đóng cửa/đóng cửa, nên cách trường này xử lý ngày giao dịch không hưởng quyền chưa được kiểm chứng.")
    cases = ", ".join(f"{c['symbol']} {c['tradingDate']}" for c in info["flagged"][:10])
    return (f"- **Điều chỉnh quyền:** {ref}. Có {len(info['flagged'])}/{info['compared']} dòng `priceChangePercent` lệch quá {limit} điểm % "
            f"so với đóng cửa/đóng cửa ({cases}). Cần đối chiếu với lịch giao dịch không hưởng quyền.")


def write_evidence(result, folder, frame=None):
    """Freeze exact input rows and configuration alongside the recomputable evidence."""
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)
    manifest = {"generated_at": datetime.now(timezone.utc).isoformat(), "ranking_method": METHOD,
                "validation_method": result["method"], "foreign": result["foreign"],
                "group": result["group"], "weights": {k: WEIGHTS[k] for k in result["weights"]},
                "top_n": result["top_n"], "calendar": result["calendar"],
                "scope": "Retrospective reconstruction of collected members, not point-in-time historical VN30 membership.",
                "date_from": result["date_from"], "date_to": result["date_to"]}
    if frame is not None:
        selected = frame[frame["index_group"] == result["group"]].sort_values(["tradingDate", "symbol"])
        records = [{k: None if pd.isna(v) else v for k, v in row.items()} for row in selected.to_dict("records")]
        payload = json.dumps(records, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False).encode("utf-8")
        (folder / "input_daily.json").write_bytes(payload)
        manifest.update({"input_file": "input_daily.json", "input_sha256": hashlib.sha256(payload).hexdigest(),
                         "rows": len(selected), "sources": sorted(selected["source"].unique().tolist()) if "source" in selected else ["unspecified"],
                         "members_by_date": {day: sorted(part["symbol"].tolist()) for day, part in selected.groupby("tradingDate")},
                         "fetched_at_values": sorted(selected["fetched_at"].dropna().unique().tolist()) if "fetched_at" in selected else []})
    from importlib.metadata import version
    manifest["libraries"] = {name: version(name) for name in ("numpy", "pandas")}
    root = Path(__file__).resolve().parents[2]
    manifest["code_sha256"] = {name: hashlib.sha256((root / name).read_bytes()).hexdigest()
                               for name in ("src/ranking/daily.py", "src/ranking/engine.py", "src/analytics/validation.py", "src/analytics/screening.py")}
    (folder / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2, allow_nan=False), encoding="utf-8")
    (folder / "evaluation.json").write_text(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False), encoding="utf-8")
    lines = ["# Kiểm chứng phương pháp daily-v2", "",
             f"Rổ {result['group']}; {result['sessions']} phiên từ {result['date_from']} đến {result['date_to']}; "
             f"{result['pairs']} cặp liền phiên được xét, {len(result['skipped_pairs'])} khoảng trống bị bỏ.", "",
             f"Khối ngoại theo **{result['foreign']}**, cân bằng (mua − bán)/(mua + bán).",
             "Dữ liệu được phân tích hồi cứu theo danh sách thành viên lúc thu thập; chưa phải kiểm thử đầu tư theo thông tin sẵn có trong quá khứ.",
             "Nguồn và mã SHA-256 của dữ liệu đầu vào: manifest.json. Dữ liệu giữ cả thời gian thu thập khi có.", "",
             "## Quy tắc đánh giá", "",
             "- Top 5 gồm mọi mã đồng điểm tại ranh giới thứ 5; Bottom 5 tương tự. Không dùng thứ tự chữ cái để phá hòa.",
             "- Chốt danh sách từ ngày t trước khi ghép lợi suất ngày sau. Thiếu lợi suất của thành viên: không tính chênh lệch Top–Bottom, không thay mã.",
             "- Nếu hai nhóm giao nhau do đồng điểm: không tính chênh lệch. IC dùng các mã đủ lợi suất, báo số mã và mã bị thiếu trong tệp chi tiết.",
             "- IC từng yếu tố và điểm tổng hợp dùng cùng tập mã. Không tính t, ngưỡng ý nghĩa hay số phiên đủ để phát hiện hiệu ứng.",
             "- " + result["calendar"]["note"], "",
             "## Lợi suất mở cửa–đóng cửa phiên kế tiếp", "",
             "Chỉ là phép mô tả bổ sung; chưa mô phỏng khớp lệnh, chu kỳ thanh toán, chi phí hay khả năng giao dịch thực tế.", "",
             "| Cấu hình | Cặp có IC | IC trung bình | Độ lệch chuẩn IC | Cặp có chênh lệch | Top–Bottom (điểm %) |",
             "|---|---:|---:|---:|---:|---:|"]
    series = []
    sensitivity = []
    for name, part in result["weights"].items():
        ic, spread = part["ic"], part["top_minus_bottom_pp"]
        lines.append(f"| {name} | {ic['pairs']} | {_fmt(ic['mean'])} | {_fmt(ic['sd'], sign=False)} | {spread['pairs']} | {_fmt(spread['mean'])} |")
        series.extend({"weights": name, **row} for row in part["pairs"])
        sensitivity.extend({"weights": name, **row} for row in part["screening"]["details"])
    pd.DataFrame(series).to_csv(folder / "kiem_tra_phien_ke_tiep.csv", index=False, encoding="utf-8-sig")
    pd.DataFrame(sensitivity).to_csv(folder / "do_nhay_sang_loc.csv", index=False, encoding="utf-8-sig")
    lines += ["", "## Độ nhạy danh sách theo dõi", "",
              "Jaccard = số mã giao / số mã hợp (0–1). Bỏ yếu tố và đổi trọng số giữ nguyên tập mã hợp lệ.",
              "Che một đầu vào bắt buộc cho từng mã rồi chấm lại nhóm còn lại; đây là tình huống thử, không phải lỗi dữ liệu thực tế. "
              "Kết quả chi tiết có cả so sánh Top trên các mã chung để tách ảnh hưởng loại mã và đổi phân vị.", "",
              "| Cấu hình | Loại | Biến thể | Số tình huống | Jaccard TB | Jaccard nhỏ nhất | Số tình huống đổi Top | Mã ra TB | Mã vào TB |",
              "|---|---|---|---:|---:|---:|---:|---:|---:|"]
    for name, part in result["weights"].items():
        for item in part["screening"]["summary"]:
            lines.append(f"| {name} | {item['kind']} | {item['name']} | {item['scenarios']} | "
                         f"{_fmt(item['mean_jaccard'], sign=False)} | {_fmt(item['min_jaccard'], sign=False)} | "
                         f"{item['changed_scenarios']} | {_fmt(item['mean_removed'], sign=False)} | {_fmt(item['mean_added'], sign=False)} |")
    lines += ["", "## Diễn giải", ""]
    lines.extend(f"- {name}: {verdict(part)}" for name, part in result["weights"].items())
    lines += [adjustment_note(result["adjustment"]), "",
              "Thay đổi công thức là phiên bản phương pháp mới; các kết quả daily-v1 không được dùng để chứng minh daily-v2.",
              "Dữ liệu, cấu hình, danh sách Top/Bottom, các ca thiếu và toàn bộ phép so sánh nằm trong evaluation.json.", ""]
    (folder / "KIEM_TRA_PHIEN_KE_TIEP.md").write_text("\n".join(lines), encoding="utf-8")
