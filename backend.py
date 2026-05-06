import pandas as pd
from datetime import datetime
import streamlit as st
from streamlit_gsheets import GSheetsConnection


COLS = ["학번", "이름", "퀴즈 점수", "마지막 접속"]


def get_gsheet_conn():
    return st.connection("gsheets", type=GSheetsConnection)


def _read_raw_df():
    """시트에서 원본 DataFrame을 읽어옵니다."""
    try:
        conn = get_gsheet_conn()
        df = conn.read(worksheet="Sheet1", ttl=0)
        if df.empty or len(df.columns) < 4:
            return pd.DataFrame(columns=COLS)
        return df
    except Exception as e:
        st.error(f"⚠️ 구글 시트 읽기 실패: {e}")
        return pd.DataFrame(columns=COLS)


def _write_df(df):
    """DataFrame 전체를 시트에 씁니다 (streamlit-gsheets-connection 사용)."""
    try:
        conn = get_gsheet_conn()
        conn.update(data=df, worksheet="Sheet1")
        return True
    except Exception as e:
        err_msg = f"구글 시트 저장 실패: {e}"
        st.session_state["_gsheet_error"] = err_msg
        return False


def append_to_gsheet(data_list):
    """구글 시트에 한 행을 추가합니다 (읽기→추가→쓰기)."""
    df = _read_raw_df()
    new_row = pd.DataFrame([data_list], columns=COLS)
    df = pd.concat([df, new_row], ignore_index=True)
    return _write_df(df)


def get_all_students_df():
    df = _read_raw_df()
    df = df.dropna(how="all")
    df["학번"] = df["학번"].astype(str).str.replace(".0", "", regex=False)
    if not df.empty:
        df = df.sort_values(by="마지막 접속", ascending=True)
        df = df.groupby("학번", as_index=False).last()
    return df


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
