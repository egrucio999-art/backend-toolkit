"""SQLite manager for clients, jobs and logs."""
import sqlite3
import os
import time


class DatabaseManager:
    def __init__(self, db_path):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.init_tables()

    def init_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS clients (
                id TEXT PRIMARY KEY,
                ip TEXT,
                hostname TEXT,
                os TEXT,
                first_seen REAL,
                last_seen REAL,
                status TEXT DEFAULT 'online'
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                client_id TEXT,
                command TEXT,
                output TEXT,
                status TEXT,
                timestamp REAL
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                level TEXT,
                message TEXT,
                timestamp REAL
            )
        """)
        self.conn.commit()

    def add_client(self, client_id, ip, hostname='', os_info=''):
        current_time = time.time()
        self.cursor.execute("""
            INSERT OR REPLACE INTO clients (id, ip, hostname, os, first_seen, last_seen, status)
            VALUES (?, ?, ?, ?, COALESCE((SELECT first_seen FROM clients WHERE id = ?), ?), ?, 'online')
        """, (client_id, ip, hostname, os_info, client_id, current_time, current_time))
        self.conn.commit()

    def get_clients(self):
        self.cursor.execute('SELECT * FROM clients ORDER BY last_seen DESC')
        return self.cursor.fetchall()

    def add_job(self, client_id, command, output='', status='pending'):
        self.cursor.execute("""
            INSERT INTO jobs (client_id, command, output, status, timestamp)
            VALUES (?, ?, ?, ?, ?)
        """, (client_id, command, output, status, time.time()))
        self.conn.commit()

    def get_jobs(self, client_id=None):
        if client_id:
            self.cursor.execute('SELECT * FROM jobs WHERE client_id = ? ORDER BY timestamp DESC', (client_id,))
        else:
            self.cursor.execute('SELECT * FROM jobs ORDER BY timestamp DESC')
        return self.cursor.fetchall()

    def add_log(self, level, message):
        self.cursor.execute("""
            INSERT INTO logs (level, message, timestamp)
            VALUES (?, ?, ?)
        """, (level, message, time.time()))
        self.conn.commit()

    def close(self):
        self.conn.close()
