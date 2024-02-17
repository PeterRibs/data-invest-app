import sqlite3
import pandas as pd


class Database:
    def __init__(self, db_name):
        self.db = db_name
        self.conn = None

    def connection_database(self):
        try:
            if self.conn is None:
                self.conn = sqlite3.connect(self.db)
        except sqlite3.Error as e:
            print(e)
        return self.conn

    def create_table(self):
        self.conn = self.connection_database()
        try:
            sql = """CREATE TABLE IF NOT EXISTS tricker_comments (
                        id INTEGER PRIMARY KEY,
                        date_time DATETIME DEFAULT CURRENT_TIMESTAMP,
                        period TEXT NOT NULL,
                        area_commented TEXT NOT NULL,
                        tricker_symbol TEXT NOT NULL,
                        comment TEXT NOT NULL
                    )"""
            self.conn.execute(sql)
        except sqlite3.Error as e:
            print(e)

    def insert_comment(self, period, area_commented, tricker_symbol, comment):
        sql = """INSERT INTO tricker_comments(date_time, period, area_commented, tricker_symbol, comment) 
                 VALUES(CURRENT_TIMESTAMP, ?, ?, ?, ?)"""
        cur = self.conn.cursor()
        cur.execute(sql, (period, area_commented, tricker_symbol, comment))
        self.conn.commit()

    def get_comments(self, tricker_symbol):
        cur = self.conn.cursor()
        cur.execute(
            "SELECT * FROM tricker_comments WHERE tricker_symbol LIKE ?",
            ("%" + tricker_symbol + "%",),
        )
        rows = cur.fetchall()
        return rows

    def get_comments_as_dataframe(self, tricker_symbol):
        cur = self.conn.cursor()
        cur.execute(
            "SELECT * FROM tricker_comments WHERE tricker_symbol LIKE ?",
            ("%" + tricker_symbol + "%",),
        )
        rows = cur.fetchall()

        column_names = [description[0] for description in cur.description]

        df = pd.DataFrame(rows, columns=column_names)
        return df
