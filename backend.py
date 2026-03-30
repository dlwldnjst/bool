# backend.py
import sqlite3
import pandas as pd
from datetime import datetime
import os

import streamlit as st

DB_PATH = 'students.db'

@st.cache_resource
def get_db_connection():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def init_db():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT UNIQUE,
            name TEXT,
            last_login TEXT,
            score INTEGER DEFAULT 0
        )
    ''')
    conn.commit()


def login_student(student_id, name):
    conn = get_db_connection()
    c = conn.cursor()
    nowStr = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Try inserting. If exists, update login time.
    c.execute('SELECT * FROM students WHERE student_id = ?', (student_id,))
    row = c.fetchone()
    
    if row:
        c.execute('UPDATE students SET last_login = ?, name = ? WHERE student_id = ?', (nowStr, name, student_id))
    else:
        c.execute('INSERT INTO students (student_id, name, last_login) VALUES (?, ?, ?)', (student_id, name, nowStr))
        
    conn.commit()

def update_score(student_id, new_score):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT score FROM students WHERE student_id = ?', (student_id,))
    row = c.fetchone()
    current_score = row[0] if row else 0
    if new_score > current_score:
        c.execute('UPDATE students SET score = ? WHERE student_id = ?', (new_score, student_id))
    conn.commit()

def get_all_students():
    conn = get_db_connection()
    df = pd.read_sql_query('SELECT student_id as "학번", name as "이름", score as "퀴즈 점수", last_login as "마지막 접속" FROM students ORDER BY last_login DESC', conn)
    return df

# Initialize DB on import
init_db()
