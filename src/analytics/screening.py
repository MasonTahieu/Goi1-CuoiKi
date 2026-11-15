"""Descriptive screening sensitivity. No weights are selected from future returns."""
import pandas as pd

from src.ranking.daily import FACTORS, WEIGHTS, rank_daily
from src.ranking.engine import percentile


def shortlist(scores, n=5, largest=True):
    """Include every tie at the nth boundary; symbol order never selects members."""
    scores = scores.dropna()
    if scores.empty:
        return []
    ordered = scores.sort_values(ascending=not largest)
    cutoff = ordered.iloc[min(n, len(ordered)) - 1]
    selected = scores[scores >= cutoff] if largest else scores[scores <= cutoff]
    return sorted(selected.index.tolist())


def compare_scores(base, other, n=5):
    a, b = set(shortlist(base, n)), set(shortlist(other, n))
    common = base.dropna().index.intersection(other.dropna().index)
    x, y = base.loc[common], other.loc[common]
    corr = float(x.rank().corr(y.rank())) if len(common) >= 3 and x.nunique() > 1 and y.nunique() > 1 else None
    return {"base_top": sorted(a), "other_top": sorted(b), "base_size": len(a), "other_size": len(b),
            "overlap": len(a & b), "jaccard": len(a & b) / len(a | b) if a | b else None,
            "removed": sorted(a - b), "added": sorted(b - a), "common_size": len(common), "rank_correlation": corr}


def screening_check(frame, group="VN30", weights="balanced", foreign="value", top_n=5):
    data = frame[frame["index_group"] == group]
    rows, excluded = [], []
    for day, session in data.groupby("tradingDate", sort=True):
        ranked = rank_daily(session.to_dict("records"), weights=weights, foreign=foreign).set_index("symbol")
        view = ranked.dropna(subset=["total_score"])
        if view.empty:
            excluded.append({"date": day, "reason": "Chưa đủ mã có đầy đủ yếu tố"})
            continue
        base = view["total_score"]
        def record(kind, name, other, **extra):
            rows.append({"date": day, "kind": kind, "name": name, "cohort_size": len(view),
                         **compare_scores(base, other.round(10), top_n), **extra})
        for factor in FACTORS:
            record("single_factor", factor, view[f"score_{factor}"])
            remaining = {k: v for k, v in WEIGHTS[weights].items() if k != factor}
            record("ablation", factor, sum(view[f"score_{k}"] * v for k, v in remaining.items()) / sum(remaining.values()))
        for name, weight_map in WEIGHTS.items():
            if name != weights:
                record("weights", name, sum(view[f"score_{k}"] * v for k, v in weight_map.items()))
        # Prespecified +/- 10 percentage points before normalizing; never optimized.
        for factor in FACTORS:
            for delta in (-0.1, 0.1):
                weight_map = dict(WEIGHTS[weights])
                weight_map[factor] += delta
                total = sum(weight_map.values())
                weight_map = {k: v / total for k, v in weight_map.items()}
                record("weights", f"{factor}{delta:+.1f}",
                       sum(view[f"score_{k}"] * v for k, v in weight_map.items()), weights=weight_map)
        # Mask one required foreign observation for each member. Complete-case exclusion removes
        # that stock, then all percentiles must be recomputed on survivors, not simply sliced.
        for symbol in sorted(view.index):
            survivors = view.drop(index=symbol)
            if len(survivors) < 10:
                record("missing", symbol, pd.Series(dtype=float), unranked=True)
                continue
            rescored = {"momentum": percentile(survivors["momentum"]),
                        "liquidity": percentile(survivors["turnover"]),
                        "foreign": percentile(survivors["foreign_ratio"])}
            score = sum(rescored[k] * v for k, v in WEIGHTS[weights].items()).round(10)
            record("missing", symbol, score, unranked=False,
                   common_top_comparison=compare_scores(base.loc[survivors.index], score, top_n))
    summary = []
    if rows:
        table = pd.DataFrame(rows)
        # Missingness is summarized over stock-day masking scenarios, not independent sessions.
        table["summary_name"] = table.apply(lambda r: "one_missing_member" if r["kind"] == "missing" else r["name"], axis=1)
        for (kind, name), part in table.groupby(["kind", "summary_name"], sort=True):
            corr = part["rank_correlation"].dropna()
            summary.append({"kind": kind, "name": name, "scenarios": len(part),
                            "mean_jaccard": float(part["jaccard"].mean()),
                            "min_jaccard": float(part["jaccard"].min()),
                            "mean_rank_correlation": float(corr.mean()) if len(corr) else None,
                            "changed_scenarios": int((part["jaccard"] < 1).sum()),
                            "mean_removed": float(part["removed"].map(len).mean()),
                            "mean_added": float(part["added"].map(len).mean())})
    return {"weights": weights, "foreign": foreign, "top_n": top_n, "summary": summary,
            "details": rows, "excluded_sessions": excluded,
            "note": "Độ nhạy mô tả, không chứng minh lợi nhuận. Top 5 gồm mọi mã đồng điểm ở ranh giới; "
                    "Jaccard = giao / hợp. Bỏ yếu tố dùng cùng tập mã hợp lệ. Thiếu dữ liệu là thử nghiệm che từng mã, "
                    "không phải tần suất lỗi thực tế."}
