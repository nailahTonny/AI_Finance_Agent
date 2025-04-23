import sqlite3
from datetime import datetime
import json

def log_to_db(intent, input_text, response, metadata=""):
    conn = sqlite3.connect("logs/activity_log.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO logs (timestamp, intent, input_text, response, metadata)
        VALUES (?, ?, ?, ?, ?)""",
        (str(datetime.now()), intent, input_text, json.dumps(response), metadata))
    conn.commit()
    conn.close()
