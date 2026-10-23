import os
import hashlib
from contextlib import contextmanager
import pyodbc
from dotenv import load_dotenv

load_dotenv()

SERVER = os.getenv("DB_SERVER", "109.233.236.26")
DATABASE = os.getenv("DB_NAME", "")
USERNAME = os.getenv("DB_USER", "")
PASSWORD = os.getenv("DB_PASSWORD", "")
DRIVER = os.getenv("DB_DRIVER", "ODBC Driver 17 for SQL Server")

def get_connection():
    conn_str = (
        f"DRIVER={{{DRIVER}}};"
        f"SERVER={SERVER};"
        f"DATABASE={DATABASE};"
        f"UID={USERNAME};"
        f"PWD={PASSWORD};"
        "TrustServerCertificate=yes;"
    )
    try:
        return pyodbc.connect(conn_str, timeout=5)
    except pyodbc.Error as e:
        print("Ошибка подключения:", e)
        return None

if __name__ == "__main__":
    conn = get_connection()
    print("Подключено!" if conn else "Не подключено")