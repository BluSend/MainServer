import sqlite3 as sq3
import random as r

db = sq3.connect("database.db")
cur = db.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS User(name TEXT, roomNumber TEXT, user_id INTEGER, email TEXT)")

def check_user(email):
    check_cur = db.cursor()
    check_cur.execute("SELECT 1 FROM User WHERE email = ? LIMIT 1", (email,))
    return check_cur.fetchone() != None

def retrieve_user(id):
    retrieve_cur = db.cursor()
    retrieve_cur.execute("SELECT name, roomNumber, user_id, email FROM User WHERE user_id = ?", (id,))
    return retrieve_cur.fetchone()

def add_user(name, roomNumber, email):
    if check_user(email):
        raise Exception("User already exists")
    else:
        cur.execute(
            "INSERT INTO User VALUES (?, ?, ?, ?)",
            (name, roomNumber, r.randint(0, 999999), email),
        )
        db.commit()
    return "User Created"
