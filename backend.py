import pandas as pd
from datetime import datetime
import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from streamlit_gsheets import GSheetsConnection

def get_gsheet_conn():
    return st.connection("gsheets", type=GSheetsConnection)

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

def get_gspread_client():
    """gspread 클라이언트를 반환합니다."""
    creds_info = dict(st.secrets["connections"]["gsheets"])
    # TOML의 \n 문자를 처리하기 위해 필요시 처리 (보통 st.secrets가 알아서 해줌)
    creds = Credentials.from_service_account_info(creds_info, scopes=SCOPES)
    return gspread.authorize(creds)

def append_to_gsheet(data_list):
    """구글 시트의 마지막에 한 행을 추가합니다 (원자적 작업)."""
    try:
        client = get_gspread_client()
        url = st.secrets["connections"]["gsheets"]["spreadsheet"]
        sh = client.open_by_url(url)
        worksheet = sh.worksheet("Sheet1")
        worksheet.append_row(data_list)
    except Exception as e:
        st.error(f"⚠️ 구글 시트에 행을 추가하는 중 오류가 발생했습니다: {e}")

def get_all_students_df():
    try:
        conn = get_gsheet_conn()
        df = conn.read(worksheet="Sheet1", ttl=0) # 항상 최신 데이터를 읽어옵니다
        
        if df.empty or len(df.columns) < 4:
            return pd.DataFrame(columns=["학번", "이름", "퀴즈 점수", "마지막 접속"])
            
        df = df.dropna(how="all")
        df["학번"] = df["학번"].astype(str).str.replace(".0", "", regex=False)
        
        # 로그 방식 대응: 학번별로 가장 최근 데이터만 남깁니다.
        if not df.empty:
            # 마지막 접속 시간을 기준으로 정렬 후 가장 마지막 항목 선택
            df = df.sort_values(by="마지막 접속", ascending=True)
            df = df.groupby("학번", as_index=False).last()
            
        return df
    except Exception as e:
        st.error(f"⚠️ 구글 시트 데이터를 읽지 못했습니다: {e}")
        return pd.DataFrame(columns=["학번", "이름", "퀴즈 점수", "마지막 접속"])

def login_student(student_id, name):
    student_id = str(student_id)
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 새로운 접속 로그를 추가합니다.
    # 기존 데이터를 읽어서 수정하지 않고 단순히 추가만 하므로 충돌이 발생하지 않습니다.
    append_to_gsheet([student_id, name, 0, now_str])

def update_score(student_id, new_score):
    student_id = str(student_id)
    # 현재 점수를 확인하기 위해 최신 데이터를 읽어옵니다 (필터링된 데이터)
    df = get_all_students_df()
    
    mask = df["학번"] == student_id
    if mask.any():
        current_score = df.loc[mask, "퀴즈 점수"].values[0]
        name = df.loc[mask, "이름"].values[0]
        try:
            current_score = int(current_score) if pd.notna(current_score) else 0
        except ValueError:
            current_score = 0
            
        # 최고 점수를 갱신했을 때만 새로운 행을 추가합니다.
        if new_score > current_score:
            now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            append_to_gsheet([student_id, name, new_score, now_str])

def get_all_students():
    df = get_all_students_df()
    if not df.empty:
        df = df.sort_values(by="마지막 접속", ascending=False)
    return df
