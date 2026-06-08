#!/usr/bin/env python3
"""
STR Scout Hub server — static file serving + dismiss/undismiss POST endpoints.
Replaces plain python3 -m http.server so the Mansfield × button and SMS agent
features continue to work after migration from the old scout-server.py on 8753.
"""

import json
import os
import sys
from http.server import SimpleHTTPRequestHandler, HTTPServer
from pathlib import Path

DISMISSED_FILE = Path(os.environ.get("SCOUT_DIR", Path.home() / "STR-Scouts")) / "dismissed.json"


def load_dismissed():
    try:
        return json.loads(DISMISSED_FILE.read_text())
    except Exception:
        return {}


def save_dismissed(data):
    DISMISSED_FILE.write_text(json.dumps(data, indent=2))


class ScoutHandler(SimpleHTTPRequestHandler):

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length) if length else b"{}"
        try:
            payload = json.loads(body)
        except Exception:
            payload = {}

        if self.path in ("/dismiss", "/undismiss"):
            dismissed = load_dismissed()
            item_id = payload.get("id") or payload.get("key") or payload.get("url") or ""

            if self.path == "/dismiss":
                dismissed[item_id] = True
            else:
                dismissed.pop(item_id, None)

            save_dismissed(dismissed)
            self._json(200, {"ok": True, "id": item_id, "dismissed": self.path == "/dismiss"})

        elif self.path == "/dismissed":
            self._json(200, load_dismissed())

        else:
            self._json(404, {"error": "Unknown endpoint"})

    def _json(self, code, data):
        body = json.dumps(data).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def log_message(self, fmt, *args):
        # suppress noisy GET logs; keep errors
        if args and str(args[1]) not in ("200", "304"):
            super().log_message(fmt, *args)


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8754
    serve_dir = os.environ.get("SCOUT_DIR", str(Path.home() / "STR-Scouts"))
    os.chdir(serve_dir)
    print(f"STR Scout Hub serving {serve_dir} on port {port}", flush=True)
    HTTPServer(("", port), ScoutHandler).serve_forever()
