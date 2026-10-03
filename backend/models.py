import sqlite3
import json
import logging
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from backend.config import Config

logger = logging.getLogger("pocketsmart.models")

def get_db_connection():
    conn = sqlite3.connect(Config.DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        name TEXT NOT NULL,
        location TEXT DEFAULT 'Mumbai, India',
        currency TEXT DEFAULT 'INR',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
    
    # User plans history table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS plan_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        planner_type TEXT NOT NULL,  -- 'home', 'party', 'jewelry'
        title TEXT NOT NULL,
        budget REAL NOT NULL,
        allocated_total REAL NOT NULL,
        estimated_spend REAL NOT NULL,
        contingency REAL NOT NULL,
        inputs_json TEXT NOT NULL,
        result_json TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
    );
    """)
    
    # Saved recommendation items
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS saved_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        plan_id INTEGER,
        planner_type TEXT NOT NULL,
        item_name TEXT NOT NULL,
        category TEXT NOT NULL,
        estimated_price REAL NOT NULL,
        platform TEXT NOT NULL,
        platform_url TEXT,
        tag TEXT,
        reason TEXT,
        image_url TEXT,
        saved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,
        FOREIGN KEY(plan_id) REFERENCES plan_history(id) ON DELETE SET NULL
    );
    """)
    
    # Seed a default demo user if not exists
    cursor.execute("SELECT id FROM users WHERE email = ?", ("demo@pocketsmart.ai",))
    if not cursor.fetchone():
        hashed = generate_password_hash("pocketsmart123")
        cursor.execute(
            "INSERT INTO users (email, password_hash, name, location, currency) VALUES (?, ?, ?, ?, ?)",
            ("demo@pocketsmart.ai", hashed, "Alexander Vance", "Bangalore, India", "INR")
        )
    
    conn.commit()
    conn.close()
    logger.info("Database initialized successfully.")

# User Model Helper Functions
def create_user(email, password, name, location="Mumbai, India", currency="INR"):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        password_hash = generate_password_hash(password)
        cursor.execute(
            "INSERT INTO users (email, password_hash, name, location, currency) VALUES (?, ?, ?, ?, ?)",
            (email.lower().strip(), password_hash, name.strip(), location, currency)
        )
        conn.commit()
        user_id = cursor.lastrowid
        return get_user_by_id(user_id)
    except sqlite3.IntegrityError:
        return None
    finally:
        conn.close()

def authenticate_user(email, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ?", (email.lower().strip(),))
    user = cursor.fetchone()
    conn.close()
    if user and check_password_hash(user["password_hash"], password):
        return dict(user)
    return None

def get_user_by_id(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, email, name, location, currency, created_at FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return dict(user) if user else None

def update_user_profile(user_id, name, location, currency):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET name = ?, location = ?, currency = ? WHERE id = ?",
        (name, location, currency, user_id)
    )
    conn.commit()
    conn.close()
    return get_user_by_id(user_id)

# History helper functions
def save_plan_history(user_id, planner_type, title, budget, allocated_total, estimated_spend, contingency, inputs_dict, result_dict):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO plan_history (
            user_id, planner_type, title, budget, allocated_total, estimated_spend, contingency, inputs_json, result_json
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        user_id,
        planner_type,
        title,
        float(budget),
        float(allocated_total),
        float(estimated_spend),
        float(contingency),
        json.dumps(inputs_dict),
        json.dumps(result_dict)
    ))
    conn.commit()
    plan_id = cursor.lastrowid
    conn.close()
    return plan_id

def get_user_plan_history(user_id=None, limit=50):
    conn = get_db_connection()
    cursor = conn.cursor()
    if user_id:
        cursor.execute("SELECT * FROM plan_history WHERE user_id = ? ORDER BY created_at DESC LIMIT ?", (user_id, limit))
    else:
        cursor.execute("SELECT * FROM plan_history ORDER BY created_at DESC LIMIT ?", (limit,))
    rows = cursor.fetchall()
    conn.close()
    
    results = []
    for r in rows:
        d = dict(r)
        try:
            d["inputs"] = json.loads(d["inputs_json"])
            d["result"] = json.loads(d["result_json"])
        except Exception:
            d["inputs"] = {}
            d["result"] = {}
        results.append(d)
    return results

def get_plan_by_id(plan_id, user_id=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    if user_id:
        cursor.execute("SELECT * FROM plan_history WHERE id = ? AND user_id = ?", (plan_id, user_id))
    else:
        cursor.execute("SELECT * FROM plan_history WHERE id = ?", (plan_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        d = dict(row)
        d["inputs"] = json.loads(d["inputs_json"])
        d["result"] = json.loads(d["result_json"])
        return d
    return None

def delete_plan(plan_id, user_id=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    if user_id:
        cursor.execute("DELETE FROM plan_history WHERE id = ? AND user_id = ?", (plan_id, user_id))
    else:
        cursor.execute("DELETE FROM plan_history WHERE id = ?", (plan_id,))
    conn.commit()
    deleted = cursor.rowcount > 0
    conn.close()
    return deleted

# Saved Items Helper Functions
def save_item_to_favorites(user_id, item_data):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO saved_items (
            user_id, plan_id, planner_type, item_name, category, estimated_price, platform, platform_url, tag, reason, image_url
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        user_id,
        item_data.get("plan_id"),
        item_data.get("planner_type", "general"),
        item_data.get("name", "Unnamed Item"),
        item_data.get("category", "General"),
        float(item_data.get("estimated_price", 0)),
        item_data.get("platform", "Amazon"),
        item_data.get("link", ""),
        item_data.get("tag", "Recommended"),
        item_data.get("reason", ""),
        item_data.get("image_url", "")
    ))
    conn.commit()
    item_id = cursor.lastrowid
    conn.close()
    return item_id

def get_user_saved_items(user_id=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    if user_id:
        cursor.execute("SELECT * FROM saved_items WHERE user_id = ? ORDER BY saved_at DESC", (user_id,))
    else:
        cursor.execute("SELECT * FROM saved_items ORDER BY saved_at DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def delete_saved_item(item_id, user_id=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    if user_id:
        cursor.execute("DELETE FROM saved_items WHERE id = ? AND user_id = ?", (item_id, user_id))
    else:
        cursor.execute("DELETE FROM saved_items WHERE id = ?", (item_id,))
    conn.commit()
    deleted = cursor.rowcount > 0
    conn.close()
    return deleted
