import sqlite3
import os
from typing import List, Tuple, Optional

DB_NAME = os.getenv("DB_NAME", "birthdays.db")

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS birthdays (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            birth_date TEXT NOT NULL,
            reminder_days INTEGER NOT NULL DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

def add_birthday(chat_id: int, name: str, birth_date: str, reminder_days: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO birthdays (chat_id, name, birth_date, reminder_days)
        VALUES (?, ?, ?, ?)
    ''', (chat_id, name, birth_date, reminder_days))
    conn.commit()
    conn.close()

def get_birthdays(chat_id: int) -> List[Tuple]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, name, birth_date, reminder_days FROM birthdays
        WHERE chat_id = ?
        ORDER BY birth_date
    ''', (chat_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def delete_birthday(birthday_id: int, chat_id: int) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        DELETE FROM birthdays
        WHERE id = ? AND chat_id = ?
    ''', (birthday_id, chat_id))
    affected = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return affected

def get_all_birthdays_for_check() -> List[Tuple]:
    """Returns all birthday records to check for notifications."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, chat_id, name, birth_date, reminder_days FROM birthdays')
    rows = cursor.fetchall()
    conn.close()
    return rows
