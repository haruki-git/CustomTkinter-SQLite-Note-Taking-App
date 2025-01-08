import tkinter as tk
from tkinter import filedialog
import sqlite3

class DatabaseManager:
    def __init__(self, db_file):
        """初期化とデフォルトのデータベース設定"""
        self.current_database = db_file

    def switch_database(self, new_db_file):
        """データベースを切り替える"""
        self.current_database = new_db_file

    def get_current_database(self):
        """現在使用中のデータベースファイル名を返す"""
        return self.current_database

    def execute_query(self, query, params=()):
        """クエリを実行し結果を返す"""
        conn = sqlite3.connect(self.current_database)
        cur = conn.cursor()
        try:
            cur.execute(query, params)
            conn.commit()
        except sqlite3.Error as e:
            raise e
        finally:
            conn.close()

    def fetch_all(self, query, params=()):
        """クエリを実行しすべての結果を取得"""
        conn = sqlite3.connect(self.current_database)
        cur = conn.cursor()
        try:
            cur.execute(query, params)
            return cur.fetchall()
        except sqlite3.Error as e:
            raise e
        finally:
            conn.close()

