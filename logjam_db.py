import sqlite3
import json
import time
import os
import hashlib
import threading
import hmac

# ponytail: local SQLite file, override with LOGJAM_DB_PATH if needed
DB_PATH = os.environ.get("LOGJAM_DB_PATH", os.path.join(os.path.dirname(os.path.abspath(__file__)), "logjam_data.sqlite"))
_LOCK = threading.Lock()

def get_db():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False, timeout=10.0)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with _LOCK:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY COLLATE NOCASE,
            password_hash TEXT,
            coins REAL DEFAULT 0,
            total_earned REAL DEFAULT 0,
            prestige_count INTEGER DEFAULT 0,
            save_data TEXT DEFAULT '{}',
            created_at INTEGER,
            updated_at INTEGER
        );
        """)

        # Default test user "rush"
        rush_hash = hashlib.sha256("2694".encode()).hexdigest()
        cur.execute("SELECT username FROM users WHERE username = ?", ("rush",))
        now = int(time.time() * 1000)
        if not cur.fetchone():
            default_save = {
                "coins": 50000,
                "totalEarned": 50000,
                "prestigeCount": 0,
                "goldenAcorns": 0,
                "woodTier": 0,
                "upgrades": {"spawnRate": 3, "convSpeed": 3, "sawCount": 1}
            }
            cur.execute("""
            INSERT INTO users (username, password_hash, coins, total_earned, prestige_count, save_data, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, ("rush", rush_hash, 50000, 50000, 0, json.dumps(default_save), now, now))

        conn.commit()
        conn.close()

def _format_user(row):
    if not row:
        return None
    try:
        save = json.loads(row["save_data"] or "{}")
    except Exception:
        save = {}

    return {
        "username": row["username"],
        "passwordHash": row["password_hash"],
        "coins": float(row["coins"] or 0),
        "totalEarned": float(row["total_earned"] or 0),
        "prestigeCount": int(row["prestige_count"] or 0),
        "save": save,
        "createdAt": row["created_at"],
        "updatedAt": row["updated_at"]
    }

def get_user(username):
    if not username:
        return None
    username = str(username).strip().lower()
    with _LOCK:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username = ?", (username,))
        row = cur.fetchone()
        conn.close()
        return _format_user(row)

def save_user(data):
    if not data or not data.get("username"):
        return False, "missing username"
    username = str(data["username"]).strip().lower()
    password_hash = data.get("passwordHash") or data.get("password_hash") or ""

    save_data = data.get("save") or data.get("saveData") or {}
    coins = float(save_data.get("coins", data.get("coins", 0)))
    total_earned = float(save_data.get("totalEarned", data.get("totalEarned", 0)))
    prestige_count = int(save_data.get("prestigeCount", data.get("prestigeCount", 0)))
    save_json = json.dumps(save_data)
    now = int(time.time() * 1000)

    with _LOCK:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT password_hash, created_at FROM users WHERE username = ?", (username,))
        existing = cur.fetchone()
        if existing:
            if not password_hash:
                password_hash = existing["password_hash"]
            created_at = existing["created_at"] or now
            cur.execute("""
            UPDATE users SET
                password_hash = ?, coins = ?, total_earned = ?, prestige_count = ?, save_data = ?, updated_at = ?
            WHERE username = ?
            """, (password_hash, coins, total_earned, prestige_count, save_json, now, username))
        else:
            created_at = now
            cur.execute("""
            INSERT INTO users (username, password_hash, coins, total_earned, prestige_count, save_data, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (username, password_hash, coins, total_earned, prestige_count, save_json, created_at, now))
        conn.commit()
        conn.close()
    return True, get_user(username)

def auth_user(username, password_hash=None, password=None):
    if not username:
        return False, "missing username", None
    username = str(username).strip().lower()
    if password and not password_hash:
        password_hash = hashlib.sha256(password.encode()).hexdigest()

    user = get_user(username)
    if not user:
        new_data = {
            "username": username,
            "passwordHash": password_hash,
            "save": {
                "coins": 0,
                "totalEarned": 0,
                "prestigeCount": 0,
                "goldenAcorns": 0,
                "woodTier": 0,
                "upgrades": {}
            }
        }
        ok, created = save_user(new_data)
        return True, "registered", created

    if password_hash and user.get("passwordHash"):
        if not hmac.compare_digest(user["passwordHash"], password_hash):
            return False, "incorrect password", None

    return True, "authenticated", user

def get_leaderboard(limit=20):
    with _LOCK:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT username, coins, total_earned, prestige_count, updated_at FROM users ORDER BY total_earned DESC, coins DESC LIMIT ?", (limit,))
        rows = cur.fetchall()
        conn.close()

    return [{
        "username": r["username"],
        "coins": r["coins"],
        "totalEarned": r["total_earned"],
        "prestigeCount": r["prestige_count"],
        "updatedAt": r["updated_at"]
    } for r in rows]

init_db()
