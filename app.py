#!/usr/bin/env python3
import os
import time
import app_db
import app_conf
import app_automate
import os.path
from os import path
from flask import Flask, flash, render_template, redirect, request, url_for
# Flask App & Secrent Key
app = Flask(__name__)
app.config['SECRET_KEY'] = app_conf.INSTAPY_SECRET
# initialize database if doesn't exists
if not path.exists('instapyapi.db'):
    app_db.sqlite_init()
# Textfiles
def write_text(text_file, text_num):
    items = app_db.sqlite_fetch_all('SELECT * FROM items')
    with open(text_file, 'w+') as writer:
        for item in items:
            if item[2] == text_num:
                writer.write(''.join(f"{item[3]}\n"))
    print(text_file)
# Timestamp
def current_time():
    print(f'\tDATE\t\tTIMESTAMP')
    localtime = time.localtime()
    result = time.strftime('\t%m/%d/%Y\t%I:%M:%S %p', localtime)
    return result
# Insert
def insert(sql_content, sql_list_id):
    list_id = app_db.sqlite_fetch_id('SELECT id FROM lists WHERE title = (?)', sql_list_id)
    app_db.sqlite_execute("INSERT INTO items (list_id, content) VALUES (?, ?)", list_id, sql_content)
# Delete
def delete(sql_content, sql_id):
    app_db.sqlite_execute(f"DELETE FROM items WHERE id={sql_id}", sql_id, sql_content)
# Update
def update(sql_content, sql_id):
    app_db.sqlite_execute_update(sql_id, sql_content)
# Home Page (index.html)
@app.route('/')
def index():
    lists = {}
    items = {}
    timestamp = current_time()
    lists = app_db.sqlite_fetch_all("SELECT * FROM lists")
    items = app_db.sqlite_fetch_all("SELECT * FROM items")
    return render_template('index.html', timestamp=timestamp, lists=lists, items=items)
# Write all data to text files
@app.route('/upload/', methods=['GET', 'POST'])
def upload():
    write_text('static/txt/influencers.txt', 1)
    write_text('static/txt/hashtags.txt', 2)
    write_text('static/txt/locations.txt', 3)
    return render_template('configure.html')
# Configure Page (configure.html)
@app.route('/configure/', methods=['GET', 'POST'])
def configure():
    lists = {}
    items = {}
    timestamp = current_time()
    if request.method == 'POST':
        sql_option = request.form['option']
        sql_list_id = request.form['list']
        sql_content = request.form['content']
        sql_id = request.form['id']
        # insert, update, delete
        insert(sql_content, sql_list_id)
        delete(sql_content, sql_id)
        update(sql_content, sql_id)
        return redirect(url_for('index'))
    options = ['insert', 'update', 'delete']
    lists = app_db.sqlite_fetch_all("SELECT * FROM lists")
    items = app_db.sqlite_fetch_all("SELECT * FROM items")
    return render_template('configure.html', timestamp=timestamp, options=options, lists=lists, items=items)
# Automate Page (automate.html)
@app.route('/automation/', methods=['GET', 'POST'])
def automation():
    lists = {}
    items = {}
    timestamp = current_time()
    lists = app_db.sqlite_fetch_all("SELECT * FROM lists")
    items = app_db.sqlite_fetch_all("SELECT * FROM items")
    return render_template('automation.html', timestamp=timestamp, lists=lists, items=items)
# Automation Initialize (automate.html)
@app.route('/automate/', methods=['GET', 'POST'])
def automate():
    if request.method == 'POST':
        app_automate.start_process()
    return render_template('index.html')

