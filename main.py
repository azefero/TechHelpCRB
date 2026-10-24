import tkinter as tk
from tkinter import messagebox
from database.connection import get_connection, fetch_one


def main():
    """Точка входа: проверяет БД и открывает регистрацию или вход."""
    root = tk.Tk()
    root.withdraw()                      # прячем пустое окно

    conn = get_connection()
    if conn is None:
        messagebox.showerror("ТехПомощь", "Не удалось подключиться к базе данных.")
        root.destroy()
        return
    conn.close()

    count = fetch_one("SELECT COUNT(*) FROM Пользователи")[0]  # число пользователей
    if count == 0:
        print("Открываем окно регистрации")   # потом здесь будет RegisterView
    else:
        print("Открываем окно входа")         # потом здесь будет LoginView

    root.destroy()                       # временно, пока окон нет


if __name__ == "__main__":
    main()