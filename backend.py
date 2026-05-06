import pandas as pd
from datetime import datetime
import time as _time
import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from streamlit_gsheets import GSheetsConnection

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]


def _get_gspread_client():
    """매번 새 gspread 클라이언트를 생성합니다 (캐싱하지 않음)."""
    raw = dict(st.secrets["connections"]["gsheets"])
    # spreadsheet URL은 인증에 불필요하므로 제거
    raw.pop("spreadsheet", None)
    creds = Credentials.from_service_account_info(raw, scopes=SCOPES)
    return gspread.authorize(creds)


def _get_spreadsheet_url():
    return st.secrets["connections"]["gsheets"]["spreadsheet"]


def get_gsheet_conn():
    return st.connection("gsheets", type=GSheetsConnection)


def append_to_gsheet(data_list, max_retries=3):
    """구글 시트에 한 행을 추가합니다."""
    last_err = None
    for attempt in range(max_retries):
        try:
            client = _get_gspread_client()
            url = _get_spreadsheet_url()
            sh = client.open_by_url(url)
            worksheet = sh.worksheet("Sheet1")
            worksheet.append_row(data_list, value_input_option="USER_ENTERED")
            return True
        except gspread.exceptions.APIError as e:
            last_err = e
            if e.response.status_code == 429:  # Rate limit
                _time.sleep(2 ** (attempt + 1))
            else:
                break
        except Exception as e:
            last_err = e
            _time.sleep(1)

    # 실패 사유를 session_state에 저장 (rerun 후에도 화면에 표시하기 위함)
    err_msg = f"구글 시트 저장 실패 ({max_retries}회 재시도): {last_err}"
    st.session_state["_gsheet_error"] = err_msg
    return False


def get_all_students_df():
    try:
        conn = get_gsheet_conn()
        df = conn.read(worksheet="Sheet1", ttl=0)

        if df.empty or len(df.columns) < 4:
            return pd.DataFrame(columns=["학번", "이름", "퀴즈 점수", "마지막 접속"])

        df = df.dropna(how="all")
        df["학번"] = df["학번"].astype(str).str.replace(".0", "", regex=False)

        if not df.empty:
            df = df.sort_values(by="마지막 접속", ascending=True)
            df = df.groupby("학번", as_index=False).last()

        return df
    except Exception as e:
        st.error(f"⚠️ 구글 시트 데이터를 읽지 못했습니다: {e}")
        return pd.DataFrame(columns=["학번", "이름", "퀴즈 점수", "마지막 접속"])


def login_student(student_id, name):
    student_id = str(student_id)
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return append_to_gsheet([student_id, name, 0, now_str])


def update_score(student_id, name, new_score, prev_best_score):
    student_id = str(student_id)
    if new_score <= prev_best_score:
        return None
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return append_to_gsheet([student_id, name, new_score, now_str])


def get_all_students():
    df = get_all_students_df()
    if not df.empty:
        df = df.sort_values(by="마지막 접속", ascending=False)
    return df
