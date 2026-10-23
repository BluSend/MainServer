# BluSend
#
#
# All requirements met
# Basic functionality tests passed

import sqlite3 as sq3
import random as r

db = sq3.connect("../database.db")
cur = db.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS
    User(name TEXT,
    roomNumber TEXT NOT NULL,
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL)
    ''')

def check_user(email):
    check_cur = db.cursor()
    check_cur.execute("SELECT 1 FROM User WHERE email = ? LIMIT 1", (email,))
    return check_cur.fetchone() != None


def all_users():
    all_cur = db.cursor()
    all_cur.execute("SELECT name, roomNumber, user_id, email FROM User")
    return all_cur.fetchall()

def retrieve_user(id):
    retrieve_cur = db.cursor()
    retrieve_cur.execute("SELECT name, roomNumber, user_id, email FROM User WHERE user_id = ?", (id,))
    return retrieve_cur.fetchone()

def add_user(name, roomNumber, email):
    add_cur = db.cursor()
    if check_user(email):
        raise Exception(f"User with email: {email} already exists")
    else:
        add_cur.execute(
            "INSERT INTO User VALUES (?, ?, NULL, ?)",
            (name, roomNumber, email),
        )
        db.commit()
    return "User Created"

def remove_user(id):
    rem_cur = db.cursor()
    rem_cur.execute("DELETE FROM User WHERE user_id = ?", (id,))
    db.commit()
    return "User Deleted"
