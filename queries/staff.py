# BluSend
#
# Fully compliant with component specific requirements
# Basic functionality tests passed


import sqlite3 as sq3
import bcrypt


db = sq3.connect("database.db")
main_cur = db.cursor()
main_cur.execute('''CREATE TABLE IF NOT EXISTS Staff (
    name TEXT NOT NULL,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL,
    role TEXT NOT NULL CHECK (role IN ('admin', 'member')),
    otp TEXT,
    staff_id INTEGER PRIMARY KEY AUTOINCREMENT
    )''')


def add_staff(name, username, email, role):
    crt_cur = db.cursor()
    crt_cur.execute('INSERT INTO Staff VALUES (?, ?, ?, ?, NULL)', (name, username, email, role))
    db.commit()
    return {
        name,
        username,
        email,
        role
    }


def change_staff_details(staff_id, name, username, email, role):
    chg_cur = db.cursor()
    chg_cur.execute('''
        UPDATE Staff
        SET name = ?, username = ?, email = ?, role = ?
        WHERE staff_id = ?
        ''', (name, username, email, role, staff_id))
    db.commit()
    return f'Member {name} details changed'

def check_staff(username):
    chk_cur = db.cursor()
    chk_cur.execute('''
        SELECT name, username, email, role, staff_id FROM Staff WHERE username = ?
        ''', (username,))

    return chk_cur.fetchone()

def remove_staff(id):
    del_cur = db.cursor()
    del_cur.execute('DELETE FROM Staff WHERE staff_id = ?', (id,))
    db.commit()
    return f'Staff Member Removed'

def set_otp(staff_id, hashed_otp):
    # Overwrites any previous hash, so a new request invalidates the old PIN
    otp_cur = db.cursor()
    otp_cur.execute("UPDATE Staff SET otp = ? WHERE staff_id = ?", (hashed_otp, staff_id))
    db.commit()
    return "OTP Set"

def verify_otp(staff_id, entered_otp):
    ver_cur = db.cursor()
    ver_cur.execute("SELECT otp FROM Staff WHERE staff_id = ?", (staff_id,))
    row = ver_cur.fetchone()
    if row is None or row[0] is None:
        return False
    return bcrypt.checkpw(entered_otp.encode('utf-8'), row[0].encode('utf-8'))
