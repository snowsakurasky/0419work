import pack.modu as lib
import sqlite3

lib.create_db()
conn = sqlite3.connect('library.db')
cursor = conn.cursor()
while True:
    username = input("請輸入帳號：")
    password = input("請輸入密碼：")

    cursor.execute("SELECT * FROM users WHERE username=? AND password=?",
                   (username, password))
    user = cursor.fetchone()

    if user:
        break

lib.show_menu()

while True:
    choice = input("選擇要執行的功能(Enter離開)：")
    if choice:
        lib.open_menu(choice, conn)
    else:
        break

conn.close()
