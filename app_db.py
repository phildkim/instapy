#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import app_conf
import sqlite3 as sqlite
# sqlite3 connection from instapyapi.db
def sqlite_con():
    con = sqlite.connect('instapyapi.db')
    con.row_factory = sqlite.Row
    return con
def sqlite_con_update():
    con = sqlite.connect('instapyapi.db')
    return con
# sqlite3 initialize with new tables & lists consists: influencers, hashtags, locations
def sqlite_init():
    try:
        con = sqlite_con()
        with con:
            cur = con.cursor()
            cur.execute("DROP TABLE IF EXISTS creds")
            cur.execute("DROP TABLE IF EXISTS lists")
            cur.execute("DROP TABLE IF EXISTS items")
            cur.execute("CREATE TABLE creds(id INTEGER PRIMARY KEY, username TEXT NOT NULL, password TEXT NOT NULL)")
            cur.execute("CREATE TABLE lists(id INTEGER PRIMARY KEY AUTOINCREMENT, created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, title TEXT NOT NULL)")
            cur.execute("CREATE TABLE items(id INTEGER PRIMARY KEY AUTOINCREMENT, created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, list_id INTEGER NOT NULL, content TEXT NOT NULL, FOREIGN KEY (list_id) REFERENCES lists (id))")
            cur.execute("INSERT INTO creds (username, password) VALUES (?, ?)", (app_conf.INSTAPY_USERNAME, app_conf.INSTAPY_PASSWORD))
            row_id = cur.lastrowid
            print(f'\nCREDS ROW ID: {row_id}\n')
            cur.execute("INSERT INTO lists (title) VALUES (?)", ('influencers',))
            cur.execute("INSERT INTO lists (title) VALUES (?)", ('hashtags',))
            cur.execute("INSERT INTO lists (title) VALUES (?)", ('locations',))
            row_id = cur.lastrowid
            print(f'\nLISTS ROW ID: {row_id}\n')
            cur.execute("INSERT INTO items (list_id, content) VALUES (?, ?)", (1, 'phildkim'))
            cur.execute("INSERT INTO items (list_id, content) VALUES (?, ?)", (1, 'tcslamet'))
            cur.execute("INSERT INTO items (list_id, content) VALUES (?, ?)", (2, 'durian'))
            cur.execute("INSERT INTO items (list_id, content) VALUES (?, ?)", (3, '1234567'))
            row_id = cur.lastrowid
            print(f'\nLISTS ROW ID: {row_id}\n')
            con.commit()
    except sqlite.Error as e:
        if con:
            con.rollback()
        print(f'\n Sqlite Initialize Error: {e.args[0]}.\n')
        sys.exit(1)
    finally:
        if con:
            con.close()
"""
fetch all sql_cmd:
  - "SELECT * FROM creds"
  - "SELECT * FROM lists"
  - "SELECT * FROM items"
"""
def sqlite_fetch_all(sql_cmd):
    queries = {}
    try:
        con = sqlite_con()
        with con:
            cur = con.cursor()
            cur.execute(sql_cmd)
            queries = cur.fetchall()
    except sqlite.Error as e:
        if con:
            con.rollback()
        print(f'\n Sqlite Fetch All Error: {e.args[0]}.\n')
        sys.exit(1)
    finally:
        if con:
            con.close()
        return queries
"""
fetch by id sql_cmd & sql_title:
    - 'SELECT id FROM lists WHERE title = (?)'
    - 'SELECT id FROM items WHERE content = (?)'
"""
def sqlite_fetch_id(sql_cmd, sql_title):
    query_id = None
    try:
        con = sqlite_con()
        with con:
            cur = con.cursor()
            query_id = cur.execute(sql_cmd, (sql_title,)).fetchone()['id']
    except sqlite.Error as e:
        if con:
            con.rollback()
        print(f'\n Sqlite Fetch ID Error: {e.args[0]}.\n')
        sys.exit(1)
    finally:
        if con:
            con.close()
        return query_id
"""
sql_cmd = "INSERT INTO items (list_id, content) VALUES (?, ?)"
sql_cmd = "UPDATE items SET content=? WHERE id=?"
sql_cmd = "DELETE FROM items WHERE list_id={sql_list_id}"
sql_list_id = [1,2,3]
sql_content = [@username, #hashtags, /locations/]
"""
def sqlite_execute(sql_cmd, sql_list_id, sql_content):
    try:
        row_id = None
        con = sqlite_con()
        with con:
            cur = con.cursor()
            if sql_cmd[:6] == 'INSERT':
                cur.execute(sql_cmd, (sql_list_id, sql_content))
            else:
                cur.execute(sql_cmd)
            row_id = cur.lastrowid
            con.commit()
    except sqlite.Error as e:
        if con:
            con.rollback()
        print(f'\n Sqlite Execute: {e.args[0]}.\n')
        sys.exit(1)
    finally:
        if con:
            con.close()
        return row_id
def sqlite_execute_update(sql_list_id, sql_content):
    try:
        con = sqlite_con_update()
        with con:
            cur = con.cursor()
            cur.execute("UPDATE items SET content=? WHERE id=?", (sql_content, sql_list_id))
            con.commit()
    except sqlite.Error as e:
        if con:
            con.rollback()
        print(f'\n Sqlite Execute: {e.args[0]}.\n')
        sys.exit(1)
    finally:
        if con:
            con.close()
"""
write to text file for instapy
  - influences.txt  (1) text_file
  - hashtags.txt    (2) text_file
  - locations.txt   (3) text_file
  - text_data = '\n'.join(con.iterdump())
"""
def write_text(text_file, text_data):
    with open(text_file, 'w+') as writer:
        writer.write(text_data)
