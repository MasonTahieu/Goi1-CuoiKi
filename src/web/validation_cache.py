"""Precomputed web validation, invalidated by the actual input and calculation code.

Generate after daily ingestion with ``python -m src.web.validation_cache``.
Requests only read the bundle; a missing/stale bundle falls back to a bounded,
process-local cache. Neither path writes to the read-only deployment filesystem.
"""
import argparse
from collections import OrderedDict
from copy import deepcopy
import hashlib
import json
from pathlib import Path
from threading import Lock

from src.analytics.validation import forward_check, verdict
from src.config import PROJECT_ROOT
from src.data.daily_store import default_daily_path, read_daily
from src.ranking import daily as daily_rank

SCHEMA = 1
CODE_FILES = ("src/ranking/daily.py", "src/ranking/engine.py", "src/analytics/validation.py",
              "src/analytics/screening.py", "src/data/daily_store.py", "src/web/validation_cache.py")
BUNDLE = PROJECT_ROOT / "webdata" / "validation.json"
_memory = OrderedDict()
_lock = Lock()


def signature(frame):
    # Full records, including nulls, membership and timestamps; no rounded scores.
    ordered = frame.sort_values(["tradingDate", "index_group", "symbol"]) if not frame.empty else frame
    raw = json.dumps(ordered.to_dict("records"), sort_keys=True, ensure_ascii=False, default=str)
    code = [(name, (PROJECT_ROOT / name).read_text(encoding="utf-8")) for name in CODE_FILES]
    return {"schema": SCHEMA, "data_sha256": hashlib.sha256(raw.encode()).hexdigest(),
            "code_sha256": hashlib.sha256(json.dumps(code, ensure_ascii=False).encode()).hexdigest()}


def web_payload(result, weights, foreign):
    """The same public payload for both precomputation and on-demand checks."""
    part = result["weights"][weights]
    return {"method": result["method"], "sessions": result["sessions"], "pairs": result["pairs"],
            "top_n": result["top_n"], "returns": result["returns"], "weights": weights,
            "weights_label": daily_rank.WEIGHT_LABELS[weights], "foreign": foreign,
            "ranking_method": result["ranking_method"], "calendar": result["calendar"],
            "skipped_pairs": result["skipped_pairs"], "date_from": result["date_from"], "date_to": result["date_to"],
            "screening": {k: v for k, v in part["screening"].items() if k != "details"},
            "summary": {"ic": part["ic"], "spread": part["top_minus_bottom_pp"], "ic_close": part["ic_close"],
                        "spread_close": part["top_minus_bottom_close_pp"]},
            "factor_ic": part["factor_ic"], "series": part["pairs"], "verdict": verdict(part)}


def _digest(payload):
    return hashlib.sha256(json.dumps(payload, sort_keys=True, ensure_ascii=False, allow_nan=False).encode()).hexdigest()


def cached_validation(frame, weights, foreign, bundle_path=None):
    identity = signature(frame)
    key = (identity["schema"], identity["data_sha256"], identity["code_sha256"], weights, foreign)
    with _lock:
        if key not in _memory:
            payload = None
            try:
                bundle = json.loads(Path(bundle_path or BUNDLE).read_text(encoding="utf-8"))
                if bundle["signature"] == identity:
                    entry = bundle["results"][f"{weights}:{foreign}"]
                    candidate = entry["payload"]
                    if (candidate["weights"] == weights and candidate["foreign"] == foreign
                            and entry["sha256"] == _digest(candidate)):
                        payload = candidate
            except (OSError, ValueError, KeyError, TypeError):
                pass  # Optional acceleration: damaged/stale files never replace a fresh calculation.
            if payload is None:
                payload = web_payload(forward_check(frame, weights=(weights,), foreign=foreign), weights, foreign)
            _memory[key] = payload
            if len(_memory) > 16:
                _memory.popitem(last=False)
        _memory.move_to_end(key)
        return deepcopy(_memory[key])


def build_bundle(database, output=BUNDLE):
    frame = read_daily(database)
    if not frame.empty:
        frame = frame[frame["index_group"].eq("VN30")]
    results = {}
    for foreign in daily_rank.FOREIGN:
        result = forward_check(frame, foreign=foreign)
        for weights in daily_rank.WEIGHTS:
            payload = web_payload(result, weights, foreign)
            results[f"{weights}:{foreign}"] = {"payload": payload, "sha256": _digest(payload)}
    bundle = {"signature": signature(frame), "results": results}
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.with_suffix(output.suffix + ".tmp")
    temporary.write_text(json.dumps(bundle, ensure_ascii=False, allow_nan=False, separators=(",", ":")) + "\n", encoding="utf-8")
    temporary.replace(output)
    return bundle


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Precompute all four VN30 web validation configurations (offline).")
    parser.add_argument("--db", type=Path, default=default_daily_path())
    parser.add_argument("--output", type=Path, default=BUNDLE)
    args = parser.parse_args()
    bundle = build_bundle(args.db, args.output)
    print(json.dumps({"configurations": len(bundle["results"]), "signature": bundle["signature"]}))
