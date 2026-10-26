# BluSend
#
# Fully compliant with component specific requirements
# Basic functionality tests passed

import sqlite3 as sq3


db = sq3.connect("database.db")
db.execute("PRAGMA foreign_keys = ON")
cur = db.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS Parcel (
    user_id INTEGER NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('Added', 'Due', 'Priority', 'Delivered', 'Delivery Failed')),
    tracking_id INTEGER PRIMARY KEY AUTOINCREMENT,
    nDelivery POSITIVE_INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES User(user_id)
            ON DELETE CASCADE
            ON UPDATE CASCADE
)''')


def add_parcel(user_id):
    add_cur = db.cursor()
    add_cur.execute("INSERT INTO Parcel VALUES (?, 'Added', NULL, 0)", (user_id,))
    db.commit()
    return "Parcel Added"


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
    result = [("user_id", "status", "tracking_id", "nDelivery")] + all_cur.fetchall()
    return result
