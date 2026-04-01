# backend.py
import pandas as pd
from datetime import datetime
import streamlit as st

from streamlit_gsheets import GSheetsConnection

def get_gsheet_conn():
    return st.connection("gsheets", type=GSheetsConnection)

def get_all_students_df():
    try:
        conn = get_gsheet_conn()
        df = conn.read(worksheet="Sheet1", ttl=0) # 항상 최신 데이터를 읽어옵니다
        
        if df.empty or len(df.columns) < 4:
            return pd.DataFrame(columns=["학번", "이름", "퀴즈 점수", "마지막 접속"])
            
        df = df.dropna(how="all")
        df["학번"] = df["학번"].astype(str).str.replace(".0", "", regex=False)
        return df
    except Exception as e:
        return pd.DataFrame(columns=["학번", "이름", "퀴즈 점수", "마지막 접속"])

def login_student(student_id, name):
    student_id = str(student_id)
    df = get_all_students_df()
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    mask = df["학번"] == student_id
    if mask.any():
        df.loc[mask, "이름"] = name
        df.loc[mask, "마지막 접속"] = now_str
    else:
        new_row = pd.DataFrame([{
            "학번": student_id,
            "이름": name,
            "퀴즈 점수": 0,
            "마지막 접속": now_str
        }])
        df = pd.concat([df, new_row], ignore_index=True)
    
    conn = get_gsheet_conn()
    conn.update(worksheet="Sheet1", data=df)

def update_score(student_id, new_score):
    student_id = str(student_id)
    df = get_all_students_df()
    
    mask = df["학번"] == student_id
    if mask.any():
        current_score = df.loc[mask, "퀴즈 점수"].values[0]
        try:
            current_score = int(current_score) if pd.notna(current_score) else 0
        except ValueError:
            current_score = 0
            
        if new_score > current_score:
            df.loc[mask, "퀴즈 점수"] = new_score
            conn = get_gsheet_conn()
            conn.update(worksheet="Sheet1", data=df)

def get_all_students():
    df = get_all_students_df()
    if not df.empty:
        df = df.sort_values(by="마지막 접속", ascending=False)
    return df
