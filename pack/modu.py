import os
import csv
import json
import sqlite3


def create_db():
    '''判斷資料庫是否存在，不存在則建立資料庫library.db
        建立資料表方式參考老師sqlite3模組講義，
        忽略csv檔第一行(next())，
        參考https://blog.csdn.net/weixin_42297382/article/details/124352616'''

    db = 'library.db'
    if not os.path.isfile(db):
        try:
            conn = sqlite3.connect(db)
            cursor = conn.cursor()

            cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                username TEXT NOT NULL,
                                password TEXT NOT NULL)''')

            with open('users.csv', 'r', encoding='utf-8') as file_1:
                users = csv.reader(file_1)
                next(users)
                for row in users:
                    cursor.execute('''INSERT INTO users (username, password)
                                   VALUES (?, ?)''', ((row[0], row[1])))

            cursor.execute('''CREATE TABLE IF NOT EXISTS books (
                                book_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                title TEXT NOT NULL,
                                author TEXT NOT NULL,
                                publisher TEXT NOT NULL,
                                year INTEGER NOT NULL)''')

            with open('books.json', 'r', encoding='utf-8') as file_2:
                books = json.load(file_2)
                for book in books:
                    cursor.execute('''INSERT INTO books (title, author,
                                        publisher, year)VALUES (?, ?, ?, ?)
                                        ''', (book['title'], book['author'],
                                              book['publisher'], book['year']))
            conn.commit()
            return conn
        except Exception as e:
            print('資料庫建立失敗')
            print(f'錯誤訊息：{e}')


def show_menu():
    '''顯示執行功能表'''
    print()
    print("-------------------")
    print("    資料表 CRUD")
    print("-------------------")
    print("    1. 增加記錄")
    print("    2. 刪除記錄")
    print("    3. 修改記錄")
    print("    4. 查詢記錄")
    print("    5. 資料清單")
    print("-------------------")


def open_menu(choice, conn):
    '''輸入選項'''
    if choice == '1':
        add_record(conn)
        show_menu()
    elif choice == '2':
        delete_record(conn)
        show_menu()
    elif choice == '3':
        update_record(conn)
        show_menu()
    elif choice == '4':
        search_record(conn)
        show_menu()
    elif choice == '5':
        data_list(conn)
        show_menu()
    else:
        print("=>無效的選擇")
        show_menu()


def add_record(conn):
    '''新增書籍紀錄'''
    try:
        cursor = conn.cursor()
        print("請輸入要新增的標題：", end="")
        title = input()
        print("請輸入要新增的作者：", end="")
        author = input()
        print("請輸入要新增的出版社：", end="")
        publisher = input()
        print("請輸入要新增的年份：", end="")
        year = input()

        if not (title and author and publisher and year):
            print("=>給定的條件不足，無法進行新增作業")
        else:
            cursor.execute('''INSERT INTO books (title, author, publisher,
                            year)VALUES (?, ?, ?, ?)''',
                           (title, author, publisher, year))
            conn.commit()
            print(f"異動 {cursor.rowcount} 記錄")
            data_list(conn)
    except Exception as e:
        print('新增記錄時發生錯誤...')
        print(f'錯誤訊息為：{e}')
    finally:
        cursor.close()


def delete_record(conn):
    '''刪除書籍'''
    try:
        cursor = conn.cursor()
        print("請問要刪除哪一本書？：", end="")
        title = input()

        if not (title):
            print("=>給定的條件不足，無法進行刪除作業")
        else:
            cursor.execute("DELETE FROM books WHERE title=?", (title,))
            conn.commit()
            print(f"異動 {cursor.rowcount} 記錄")
            data_list(conn)
    except Exception as e:
        print('刪除記錄時發生錯誤...')
        print(f'錯誤訊息為：{e}')
    finally:
        cursor.close()


def update_record(conn):
    '''修改書籍紀錄'''
    try:
        cursor = conn.cursor()
        print("請問要修改哪一本書的標題？：", end="")
        title = input()

        print("請輸入要更改的標題：", end="")
        new_title = input()

        print("請輸入要更改的作者：", end="")
        new_author = input()

        print("請輸入要更改的出版社：", end="")
        new_publisher = input()

        print("請輸入要更改的年份：", end="")
        new_year = input()

        if not (title and new_title and new_author and new_publisher
                and new_year):
            print("=>給定的條件不足，無法進行修改作業")
        else:
            cursor.execute('''UPDATE books SET title=?, author=?, publisher=?,
                           year=? WHERE title=?''', (new_title, new_author,
                                                     new_publisher, new_year,
                                                     title))
            conn.commit()
            print(f"異動 {cursor.rowcount} 記錄")
            data_list(conn)
    except Exception as e:
        print('修改記錄時發生錯誤...')
        print(f'錯誤訊息為：{e}')
    finally:
        cursor.close()


def search_record(conn):
    '''搜尋紀錄'''
    try:
        cursor = conn.cursor()
        print("請輸入想查詢的關鍵字：", end="")
        keyword = input()

        cursor.execute('''SELECT title, author, publisher, year FROM books
                       WHERE title LIKE ? OR author LIKE ?''',
                       ('%' + keyword + '%', '%' + keyword + '%'))
        rows = cursor.fetchall()

        if len(rows) == 0:
            print("=>給定的條件不足，無法進行搜尋作業")
        else:
            print(f"|{'書名':{chr(12288)}^10}|"
                  f"{'作者':{chr(12288)}^10}|"
                  f"{'出版社':{chr(12288)}^10}|"
                  f"{'年分':^10}|")
            for row in rows:
                print(f"|{row[0]:{chr(12288)}<10}|"
                      f"{row[1]:{chr(12288)}<10}|"
                      f"{row[2]:{chr(12288)}<10}|"
                      f"{row[3]:{chr(12288)}<8}|")
    except Exception as e:
        print('查詢記錄時發生錯誤...')
        print(f'錯誤訊息為：{e}')
    finally:
        cursor.close()


def data_list(conn):
    '''資料庫內書籍清單'''
    try:
        cursor = conn.cursor()

        cursor.execute("SELECT title, author, publisher, year FROM books")
        rows = cursor.fetchall()

        if len(rows) == 0:
            print("資料庫中無任何記錄")
        else:
            print(f"|{'書名':{chr(12288)}^10}|"
                  f"{'作者':{chr(12288)}^10}|"
                  f"{'出版社':{chr(12288)}^10}|"
                  f"{'年分':^10}|")
            for row in rows:
                print(f"|{row[0]:{chr(12288)}<10}|"
                      f"{row[1]:{chr(12288)}<10}|"
                      f"{row[2]:{chr(12288)}<10}|"
                      f"{row[3]:{chr(12288)}<8}|")
    except Exception as e:
        print('查詢記錄時發生錯誤...')
        print(f'錯誤訊息為：{e}')
    finally:
        cursor.close()
