import sqlite3
import os

DB_PATH = "db/bot.db"
os.makedirs("db", exist_ok=True)

conn = sqlite3.connect(DB_PATH, check_same_thread=False)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    telegram_id INTEGER UNIQUE,
    name TEXT,
    language TEXT DEFAULT 'en'
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS habits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    name TEXT,
    streak INTEGER DEFAULT 0,
    goal INTEGER DEFAULT 0
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    title TEXT,
    due TEXT,
    done INTEGER DEFAULT 0
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS finance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    type TEXT,
    amount REAL,
    category TEXT,
    note TEXT
)
""")

conn.commit()

def get_user(tg):
    cur.execute("SELECT * FROM users WHERE telegram_id=?", (tg,))
    return cur.fetchone()

def create_user(tg, name, lang):
    cur.execute("INSERT INTO users (telegram_id, name, language) VALUES (?, ?, ?)", (tg, name, lang))
    conn.commit()

def set_lang(tg, lang):
    cur.execute("UPDATE users SET language=? WHERE telegram_id=?", (lang, tg))
    conn.commit()

def get_lang(tg):
    cur.execute("SELECT language FROM users WHERE telegram_id=?", (tg,))
    r = cur.fetchone()
    return r[0] if r else "en"

def get_uid(tg):
    cur.execute("SELECT id FROM users WHERE telegram_id=?", (tg,))
    r = cur.fetchone()
    return r[0] if r else None

def add_habit(uid, name):
    cur.execute("INSERT INTO habits (user_id, name) VALUES (?, ?)", (uid, name))
    conn.commit()

def list_habits(uid):
    cur.execute("SELECT id, name, streak, goal FROM habits WHERE user_id=?", (uid,))
    return cur.fetchall()

def habit_done(hid):
    cur.execute("UPDATE habits SET streak=streak+1 WHERE id=?", (hid,))
    conn.commit()

def set_goal(hid, goal):
    cur.execute("UPDATE habits SET goal=? WHERE id=?", (goal, hid))
    conn.commit()

def add_task(uid, title, due):
    cur.execute("INSERT INTO tasks (user_id, title, due) VALUES (?, ?, ?)", (uid, title, due))
    conn.commit()

def list_tasks(uid):
    cur.execute("SELECT id, title, due, done FROM tasks WHERE user_id=?", (uid,))
    return cur.fetchall()

def task_done(tid):
    cur.execute("UPDATE tasks SET done=1 WHERE id=?", (tid,))
    conn.commit()

def add_fin(uid, t_type, amount, category, note):
    cur.execute("INSERT INTO finance (user_id, type, amount, category, note) VALUES (?, ?, ?, ?, ?)",
                (uid, t_type, amount, category, note))
    conn.commit()

def finance_stats(uid):
    cur.execute("SELECT type, SUM(amount) FROM finance WHERE user_id=? GROUP BY type", (uid,))
    rows = cur.fetchall()
    income = sum(x[1] for x in rows if x[0]=="income")
    expense = sum(x[1] for x in rows if x[0]=="expense")

    cur.execute("SELECT category, SUM(amount) FROM finance WHERE user_id=? AND type='expense' GROUP BY category", (uid,))
    bycat = cur.fetchall()

    return income, expense, bycat
