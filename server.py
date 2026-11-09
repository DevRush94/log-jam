#!/usr/bin/env python3
"""
Log Jam Cloud Save Server
Matches the Wings of Fire backend architecture:
- Stdlib Python only (runs anywhere: Windows, Termux, Linux, macOS, 0 dependencies)
- Open CORS for local & Cloudflare tunnel access
- Serves static index.html game
- Full auth and cloud save endpoints
"""

import os
import sys
import json
import time
import base64
import hashlib
import hmac
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import logjam_db as db

PORT = int(os.environ.get("PORT", "8000"))
INDEX_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "index.html")

JWT_SECRET = os.environ.get("LOGJAM_JWT_SECRET", "logjam_super_secret_jwt_key_2026")
JWT_EXPIRY = 30 * 24 * 3600  # 30 days

def create_jwt(username: str) -> str:
    header = {"alg": "HS256", "typ": "JWT"}
    payload = {"sub": username.lower(), "exp": int(time.time()) + JWT_EXPIRY, "iat": int(time.time())}
    b64_h = base64.urlsafe_b64encode(json.dumps(header).encode()).decode().rstrip("=")
    b64_p = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode().rstrip("=")
    msg = f"{b64_h}.{b64_p}".encode()
    sig = base64.urlsafe_b64encode(hmac.new(JWT_SECRET.encode(), msg, hashlib.sha256).digest()).decode().rstrip("=")
    return f"{b64_h}.{b64_p}.{sig}"

def verify_jwt(token: str):
    try:
        parts = token.strip().split(".")
        if len(parts) != 3:
            return None
        b64_h, b64_p, sig = parts
        msg = f"{b64_h}.{b64_p}".encode()
        expected_sig = base64.urlsafe_b64encode(hmac.new(JWT_SECRET.encode(), msg, hashlib.sha256).digest()).decode().rstrip("=")
        if not hmac.compare_digest(sig, expected_sig):
            return None
        p_bytes = b64_p + "=" * (-len(b64_p) % 4)
        payload = json.loads(base64.urlsafe_b64decode(p_bytes.encode()).decode())
        if payload.get("exp", 0) < int(time.time()):
            return None
        return payload.get("sub")
    except Exception:
        return None

class LogJamHandler(BaseHTTPRequestHandler):
    def _cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization, X-User-Id")
        self.send_header("Access-Control-Max-Age", "86400")

    def _json(self, data, code=200):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self._cors_headers()
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        self._cors_headers()
        self.end_headers()

    def _get_auth_username(self):
        auth_header = self.headers.get("Authorization", "")
        if auth_header.lower().startswith("bearer "):
            token = auth_header[7:].strip()
            user = verify_jwt(token)
            if user:
                return user
        x_user = self.headers.get("X-User-Id", "")
        if x_user:
            return x_user.strip().lower()
        return None

    def _read_body_json(self):
        try:
            n = int(self.headers.get("Content-Length", "0"))
            if n <= 0:
                return {}
            raw = self.rfile.read(n).decode("utf-8")
            return json.loads(raw)
        except Exception:
            return None

    def do_GET(self):
        q = urllib.parse.urlparse(self.path)
        path = q.path.rstrip("/")
        if not path:
            path = "/"

        # Health & Status
        if path in ("/api/health", "/api/status", "/health"):
            return self._json({
                "ok": True,
                "service": "Log Jam Cloud Save API",
                "status": "online",
                "db": "sqlite3",
                "timestamp": int(time.time() * 1000)
            })

        # Leaderboard
        if path == "/api/leaderboard":
            return self._json({"ok": True, "leaderboard": db.get_leaderboard()})

        # Get User / Progress
        if path in ("/api/user", "/progress"):
            params = urllib.parse.parse_qs(q.query)
            uname = (params.get("username") or [""])[0]
            if not uname:
                uname = self._get_auth_username() or ""
            uname = uname.strip().lower()
            if not uname:
                return self._json({"ok": False, "error": "Username or Authorization required"}, 400)
            user = db.get_user(uname)
            if not user:
                return self._json({"ok": False, "error": "user not found"}, 404)
            return self._json({
                "ok": True,
                "user": user,
                "save": user.get("save", {}),
                "updated_at": user.get("updatedAt", int(time.time() * 1000))
            })

        # Static Game files
        if path in ("/", "/index.html", "/game", "/play", "/logjam"):
            if os.path.exists(INDEX_PATH):
                with open(INDEX_PATH, "rb") as f:
                    content = f.read()
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self._cors_headers()
                self.send_header("Content-Length", str(len(content)))
                self.end_headers()
                self.wfile.write(content)
                return
            else:
                return self._json({"ok": False, "error": "index.html not found"}, 404)

        return self._json({"ok": False, "error": "not found"}, 404)

    def do_POST(self):
        q = urllib.parse.urlparse(self.path)
        path = q.path.rstrip("/")

        data = self._read_body_json()
        if data is None:
            return self._json({"ok": False, "error": "invalid json payload"}, 400)

        # Auth endpoint (Register or Login)
        if path in ("/api/user/auth", "/register", "/login"):
            uname = str(data.get("username", "")).strip().lower()
            if not uname:
                return self._json({"ok": False, "error": "username required"}, 400)
            phash = data.get("passwordHash") or data.get("password_hash") or ""
            pwd = data.get("password", "")
            if pwd and not phash:
                phash = hashlib.sha256(pwd.encode()).hexdigest()

            ok, action, user = db.auth_user(uname, password_hash=phash, password=pwd)
            if not ok:
                return self._json({"ok": False, "error": action}, 401)

            token = create_jwt(uname)
            return self._json({
                "ok": True,
                "action": action,
                "token": token,
                "user": user,
                "save": user.get("save", {}),
                "updated_at": user.get("updatedAt", int(time.time() * 1000))
            })

        # Save endpoint
        if path in ("/api/user/save", "/progress"):
            uname = str(data.get("username", "")).strip().lower()
            if not uname:
                uname = self._get_auth_username() or ""
            if not uname:
                return self._json({"ok": False, "error": "username required"}, 400)

            user = db.get_user(uname)
            if user and user.get("passwordHash"):
                auth_user = self._get_auth_username()
                token_valid = (auth_user and auth_user == uname)
                req_hash = data.get("passwordHash") or data.get("password_hash") or ""
                hash_valid = (req_hash and hmac.compare_digest(user["passwordHash"], req_hash))
                if not (token_valid or hash_valid):
                    return self._json({"ok": False, "error": "Authentication required to update save"}, 401)

            save_content = data.get("save") or data.get("saveData") or {}
            ok, updated = db.save_user({
                "username": uname,
                "passwordHash": data.get("passwordHash") or (user.get("passwordHash") if user else ""),
                "save": save_content,
                "coins": save_content.get("coins", 0),
                "totalEarned": save_content.get("totalEarned", 0),
                "prestigeCount": save_content.get("prestigeCount", 0)
            })
            if not ok:
                return self._json({"ok": False, "error": str(updated)}, 500)

            return self._json({
                "ok": True,
                "user": updated,
                "updated_at": updated.get("updatedAt", int(time.time() * 1000))
            })

        return self._json({"ok": False, "error": "not found"}, 404)

    def do_PUT(self):
        q = urllib.parse.urlparse(self.path)
        path = q.path.rstrip("/")
        if path == "/progress":
            return self.do_POST()
        return self._json({"ok": False, "error": "not found"}, 404)

    def log_message(self, format, *args):
        sys.stderr.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {args[0]} {args[1]} -> {args[2]}\n")

def run(port=PORT):
    server_address = ("0.0.0.0", port)
    httpd = ThreadingHTTPServer(server_address, LogJamHandler)
    print(f"🌲 Log Jam server running at http://0.0.0.0:{port}")
    print(f"   Matches Wings of Fire backend architecture with full CORS and Cloudflare tunnel support.")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server.")
        httpd.server_close()

if __name__ == "__main__":
    run()
