import sqlite3
import time
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "trakr.db")

def _get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the SQLite database and create necessary tables."""
    with _get_conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS bot_state (
                bot_id TEXT PRIMARY KEY,
                offline_since REAL
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS audit_state (
                key TEXT PRIMARY KEY,
                last_audit_id TEXT
            )
        """)
        conn.commit()

def mark_offline(bot_id: str) -> None:
    """Mark a bot as offline, recording the current timestamp."""
    now = time.time()
    with _get_conn() as conn:
        conn.execute("""
            INSERT INTO bot_state (bot_id, offline_since)
            VALUES (?, ?)
            ON CONFLICT(bot_id) DO UPDATE SET offline_since=excluded.offline_since
        """, (bot_id, now))
        conn.commit()

def mark_online(bot_id: str) -> float | None:
    """
    Mark a bot as online. 
    Returns the downtime duration in seconds if it was previously offline, otherwise None.
    """
    with _get_conn() as conn:
        cur = conn.execute("SELECT offline_since FROM bot_state WHERE bot_id = ?", (bot_id,))
        row = cur.fetchone()
        
        duration = None
        if row and row["offline_since"]:
            duration = time.time() - row["offline_since"]
            
        # Reset the offline timestamp now that the bot is online
        conn.execute("""
            INSERT INTO bot_state (bot_id, offline_since)
            VALUES (?, NULL)
            ON CONFLICT(bot_id) DO UPDATE SET offline_since=NULL
        """, (bot_id,))
        conn.commit()
        
        return duration

def get_last_audit_id(guild_id: str) -> int | None:
    """Retrieve the last processed audit log ID for a guild."""
    with _get_conn() as conn:
        cur = conn.execute("SELECT last_audit_id FROM audit_state WHERE key = ?", (guild_id,))
        row = cur.fetchone()
        if row and row["last_audit_id"]:
            return int(row["last_audit_id"])
    return None

def set_last_audit_id(guild_id: str, audit_id: int) -> None:
    """Store the last processed audit log ID for a guild."""
    with _get_conn() as conn:
        conn.execute("""
            INSERT INTO audit_state (key, last_audit_id)
            VALUES (?, ?)
            ON CONFLICT(key) DO UPDATE SET last_audit_id=excluded.last_audit_id
        """, (guild_id, str(audit_id)))
        conn.commit()

# Ensure tables are created when this module is imported
init_db()
