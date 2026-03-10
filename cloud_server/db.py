import sqlite3

def get_connection():
    return sqlite3.connect("alerts.db",check_same_thread=False)

def init_db():

    c=get_connection().cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS alerts(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id TEXT,
        alert_type TEXT,
        hr INT,
        spo2 REAL,
        temp REAL,
        acc_mag REAL,
        timestamp REAL)""")

    c.execute("""CREATE TABLE IF NOT EXISTS patient_health(
        patient_id TEXT PRIMARY KEY,
        status TEXT,
        hr INT,
        spo2 REAL,
        temp REAL,
        acc_mag REAL,
        timestamp REAL)""")

    c.connection.commit()
