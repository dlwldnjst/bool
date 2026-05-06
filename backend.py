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

# service account JSON에 없어야 하는 TOML 전용 필드들
_TOML_EXTRA_KEYS = {"spreadsheet", "type"}


def _get_creds_info():
    """st.secrets에서 service account 정보만 깔끔하게 분리해서 반환합니다."""
    raw = dict(st.secrets["connections"]["gsheets"])
    return {k: v for k, v in raw.items() if k not in _TOML_EXTRA_KEYS}


def _get_spreadsheet_url():
    """구글 시트 URL을 secrets에서 가져옵니다."""
    return st.secrets["connections"]["gsheets"]["spreadsheet"]


# ------ gspread 클라이언트 캐싱 ------
# Streamlit은 매 rerun마다 모듈을 재실행하므로, @st.cache_resource로
# gspread 클라이언트와 워크시트 객체를 재사용합니다.
# 이렇게 하면 30명이 동시에 접속해도 인증 요청은 1회만 발생합니다.

@st.cache_resource
def _get_cached_client():
    """gspread 클라이언트를 캐싱하여 반환합니다 (인증 1회만 수행)."""
    creds_info = _get_creds_info()
    creds = Credentials.from_service_account_info(creds_info, scopes=SCOPES)
    return gspread.authorize(creds)


@st.cache_resource
def _get_cached_worksheet():
    """워크시트 객체를 캐싱하여 반환합니다 (매번 open_by_url 방지)."""
    client = _get_cached_client()
    url = _get_spreadsheet_url()
    sh = client.open_by_url(url)
    return sh.worksheet("Sheet1")


def get_gsheet_conn():
    """streamlit-gsheets-connection 읽기 전용 커넥션."""
    return st.connection("gsheets", type=GSheetsConnection)


def append_to_gsheet(data_list, max_retries=3):
    """구글 시트의 마지막에 한 행을 추가합니다. 실패 시 재시도합니다."""
    last_err = None
    for attempt in range(max_retries):
        try:
            worksheet = _get_cached_worksheet()
            worksheet.append_row(data_list, value_input_option="USER_ENTERED")
            return True
        except gspread.exceptions.APIError as e:
            last_err = e
            if e.response.status_code == 429:  # Rate limit
                wait = 2 ** (attempt + 1)  # 2, 4, 8초 대기
                _time.sleep(wait)
            else:
                break
        except Exception as e:
            last_err = e
            # 캐시된 연결이 만료되었을 수 있으니 캐시를 무효화하고 재시도
            if attempt == 0:
                _get_cached_worksheet.clear()
                _get_cached_client.clear()
            _time.sleep(1)

    # 모든 재시도 실패
    st.error(f"⚠️ 구글 시트 저장에 실패했습니다 (재시도 {max_retries}회). 오류: {last_err}")
    return False


def get_all_students_df():
    try:
        conn = get_gsheet_conn()
        df = conn.read(worksheet="Sheet1", ttl=0)

        if df.empty or len(df.columns) < 4:
            return pd.DataFrame(columns=["학번", "이름", "퀴즈 점수", "마지막 접속"])

        df = df.dropna(how="all")
        df["학번"] = df["학번"].astype(str).str.replace(".0", "", regex=False)

        # 로그 방식 대응: 학번별로 가장 최근 데이터만 남깁니다.
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
    """점수를 구글 시트에 기록합니다.

    prev_best_score보다 높을 때만 기록합니다 (중복 쓰기 방지).
    전체 시트를 읽지 않고 app.py 세션에서 최고 점수를 직접 전달받습니다.
    """
    student_id = str(student_id)
    if new_score <= prev_best_score:
        return None  # 갱신 필요 없음
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return append_to_gsheet([student_id, name, new_score, now_str])


def get_all_students():
    df = get_all_students_df()
    if not df.empty:
        df = df.sort_values(by="마지막 접속", ascending=False)
    return df
