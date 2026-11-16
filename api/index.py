"""Vercel Python function: the same handler as src/web/server.py behind one catch-all rewrite.

vercel.json rewrites every path to /api/index?__path=/<original path>, so the handler can
recover the path the visitor asked for whatever the platform puts in ``self.path``.
"""
from pathlib import Path
import os
import sys
from urllib.parse import parse_qsl, urlencode, urlsplit

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

# This deployment serves SSI V3 daily data and V3 OHLC only. Keep non-secret
# defaults with the entry point; credentials still come from Vercel settings.
if os.environ.get("VERCEL"):
    if os.environ.get("SSI_API_PROFILE", "").strip() in ("", "unselected"):
        os.environ["SSI_API_PROFILE"] = "fastconnect_v3"
    os.environ.setdefault("SSI_DAILY_DATABASE", "webdata/ssi_daily.sqlite")
    os.environ.setdefault("SSI_OTP_MODE", "none")

from src.web.server import Handler  # noqa: E402


def original_path(raw):
    parts = urlsplit(raw)
    query = parse_qsl(parts.query, keep_blank_values=True)
    wanted = [value for key, value in query if key == "__path"]
    if not wanted:
        return raw
    rest = [(key, value) for key, value in query if key != "__path"]
    path = wanted[-1] if wanted[-1].startswith("/") else "/" + wanted[-1]
    return path + ("?" + urlencode(rest) if rest else "")


class handler(Handler):
    daily_only = True

    def do_GET(self):
        self.path = original_path(self.path)
        return super().do_GET()
