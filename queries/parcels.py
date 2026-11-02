# BluSend
#
# Fully compliant with component specific requirements
# Basic functionality tests passed

import sqlite3 as sq3
import bcrypt


db = sq3.connect("database.db")
db.execute("PRAGMA foreign_keys = ON")
cur = db.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS Parcel (
    user_id INTEGER NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('Added', 'Due', 'Priority', 'Delivered', 'Delivery Failed')),
    tracking_id INTEGER PRIMARY KEY AUTOINCREMENT,
    nDelivery POSITIVE_INTEGER NOT NULL,
    otp TEXT,
    compartment_number INTEGER CHECK (compartment_number IN (NULL, 1, 2, 3, 4)),
    FOREIGN KEY (user_id) REFERENCES User(user_id)
            ON DELETE CASCADE
            ON UPDATE CASCADE
)''')


def add_parcel(user_id):
    add_cur = db.cursor()
    add_cur.execute("INSERT INTO Parcel VALUES (?, 'Added', NULL, 0, NULL, NULL)", (user_id,))
    db.commit()
    return "Parcel Added"

def set_otp(tracking_id, hashed_otp):
    # Overwrites any previous hash, so a new request invalidates the old PIN
    otp_cur = db.cursor()
    otp_cur.execute("UPDATE Parcel SET otp = ? WHERE tracking_id = ?", (hashed_otp, tracking_id))
    db.commit()
    return "OTP Set"

def verify_otp(tracking_id, entered_otp):
    ver_cur = db.cursor()
    ver_cur.execute("SELECT otp FROM Parcel WHERE tracking_id = ?", (tracking_id,))
    row = ver_cur.fetchone()
    if row is None or row[0] is None:
        return False
    return bcrypt.checkpw(entered_otp.encode('utf-8'), row[0].encode('utf-8'))

def change_owner(tracking_id, new_user_id):
    chg_usr_cur = db.cursor()
    chg_usr_cur.execute('''
        UPDATE Parcel
        SET user_id = ?
        WHERE tracking_id = ?
        ''', (new_user_id, tracking_id))
    db.commit()

    return f"Owner Changed, new user_id = {new_user_id}"

def change_status(tracking_id, new_status):
    chg_sta_cur = db.cursor()
    chg_sta_cur.execute('''
        UPDATE Parcel
        SET status = ?
        WHERE tracking_id = ?
        ''', (new_status, tracking_id))
    db.commit()
    return f"Status Changed to {new_status}"

def remove_parcel(tracking_id):
    del_cur = db.cursor()
    del_cur.execute('DELETE FROM Parcel WHERE tracking_id = ?', (tracking_id,))
    db.commit()
    return f"Deleted Parcel {tracking_id}"

def increment_delivery(tracking_id):
    inc_cur = db.cursor()
    inc_cur.execute('SELECT nDelivery FROM Parcel WHERE tracking_id = ?', (tracking_id,))
    current_count = inc_cur.fetchall()
    inc_cur.execute('''
        UPDATE Parcel
        SET nDelivery = ?
        WHERE tracking_id = ?
        ''', (current_count[0][0] + 1, tracking_id))
    db.commit()
    return f'Count incremented. Current count = {current_count[0][0] + 1}'

def decrement_delivery(tracking_id):
    inc_cur = db.cursor()
    inc_cur.execute('SELECT nDelivery FROM Parcel WHERE tracking_id = ?', (tracking_id,))
    current_count = inc_cur.fetchall()
    inc_cur.execute('''
        UPDATE Parcel
        SET nDelivery = ?
        WHERE tracking_id = ?
        ''', (current_count[0][0] - 1, tracking_id))
    db.commit()
    return f'Count incremented. Current count = {current_count[0][0] - 1}'

def all_parcels(user_id = None):
    all_cur = db.cursor()
    all_cur.execute(f'SELECT user_id, status, tracking_id, nDelivery FROM Parcel {"WHERE user_id = ?" if user_id  else " "}', (user_id,) if user_id else ())
    result = all_cur.fetchall()
    return result

def assign_compartment(tracking_id, compartment_number):
    ac_cur = db.cursor()
    ac_cur.execute('''
        UPDATE Parcel
        SET compartment_number = ?
        WHERE tracking_id = ?
        ''', (compartment_number, tracking_id))
    db.commit()
    return f'Compartment number updated to {compartment_number}'
