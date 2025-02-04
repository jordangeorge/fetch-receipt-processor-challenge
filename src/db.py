import sqlite3
import json

class SQLiteDB:
    def __init__(self) -> None:
        self._create_table()

    def _get_connection(self):
        conn = None
        try:
            conn = sqlite3.connect("receipts.db")
        except Exception as e:
            print(f"Error connecting to database: {e}")
            exit()
        return conn

    def _create_table(self) -> None:
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS receipts (
                id VARCHAR(100) PRIMARY KEY,
                json_data TEXT
            )
        """)
        conn.commit()
        conn.close()

    def add_receipt(self, unique_id, json_data):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO receipts
                (id, json_data)
            VALUES
                (?, ?)
            """, (
            unique_id,
            json.dumps(json_data)
        ))
        conn.commit()
        conn.close()

    def get_receipt(self, unique_id):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT json_data
            FROM receipts
            WHERE id = ?
            """, 
            (unique_id,)
        )
        row = cursor.fetchone()
        conn.close()
        return row
