"""Модуль работы с базой данных TechHelpCRB (MS SQL Server через pyodbc).

Параметры подключения читаются из файла .env, который не попадает в Git.
"""
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
    """Подключается к базе данных.

    Возвращает объект подключения pyodbc или None, если сервер недоступен
    либо неверны параметры подключения.
    """
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

@contextmanager
def get_cursor():
    """Курсор в транзакции для использования в блоке with.

    При успешном выполнении изменения сохраняются (commit), при ошибке
    отменяются (rollback), после чего курсор и подключение закрываются.
    Если подключиться не удалось, выбрасывает ConnectionError.
    """
    conn = get_connection()
    if conn is None:
        raise ConnectionError("Нет соединения с базой данных")
    cursor = conn.cursor()
    try:
        yield cursor
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()

def execute_query(query, params=None):
    """Выполняет запрос на изменение данных (INSERT, UPDATE, DELETE).

    query  — текст SQL с параметрами в виде знаков ?;
    params — кортеж значений для параметров.
    Возвращает количество изменённых строк.
    """
    with get_cursor() as cursor:
        cursor.execute(query, params or ())
        return cursor.rowcount

def hash_password(password):
    """Возвращает хеш SHA-256 пароля в виде строки из 64 символов."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def fetch_one(query, params=None):
    """Выполняет SELECT и возвращает одну строку результата или None."""
    with get_cursor() as cursor:
        cursor.execute(query, params or ())
        return cursor.fetchone()

def fetch_all(query, params=None):
    """Выполняет SELECT и возвращает список всех строк результата."""
    with get_cursor() as cursor:
        cursor.execute(query, params or ())
        return cursor.fetchall()


if __name__ == "__main__":
    print(fetch_one("SELECT COUNT(*) FROM Пользователи"))
    print(fetch_all("SELECT name FROM sys.tables"))
    print(hash_password("123456"))