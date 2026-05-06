import pandas as pd
import re
import tempfile
import json
from datetime import datetime
import streamlit as st
from streamlit_gsheets import GSheetsConnection
from google.oauth2.service_account import Credentials


COLS = ["학번", "이름", "퀴즈 점수", "마지막 접속"]


def _normalize_private_key(key_str):
    """private_key를 표준 형식으로 정규화합니다."""
    key_str = key_str.strip()
    # base64 부분만 추출 (헤더/푸터/공백 제거)
    b64 = re.sub(
        r'-----BEGIN PRIVATE KEY-----|-----END PRIVATE KEY-----|[\s\r\n]+',
        '', key_str
    )
    # 64자마다 줄바꿈하여 표준 PEM 형식으로 재조립
    lines = [b64[i:i+64] for i in range(0, len(b64), 64)]
    return "-----BEGIN PRIVATE KEY-----\n" + "\n".join(lines) + "\n-----END PRIVATE KEY-----\n"


def diagnose_connection():
    """Admin용: 구글 시트 연결 상태를 진단합니다."""
    results = []
    try:
        raw = dict(st.secrets["connections"]["gsheets"])
    except Exception as e:
        return [f"❌ secrets 읽기 실패: {e}"]

    results.append(f"✅ secrets 항목 수: {len(raw)}개")
    results.append(f"   - 키 필드: {list(raw.keys())}")

    # private_key 검사
    pk = raw.get("private_key", "")
    results.append(f"   - private_key 길이: {len(pk)}자")
    has_begin = "BEGIN PRIVATE KEY" in pk
    has_end = "END PRIVATE KEY" in pk
    results.append(f"   - BEGIN 마커: {'✅' if has_begin else '❌ 없음'}")
    results.append(f"   - END 마커: {'✅' if has_end else '❌ 없음'}")

    # 실제 newline vs 리터럴 \n 확인
    actual_newlines = pk.count('\n')
    literal_backslash_n = pk.count('\\n')
    results.append(f"   - 실제 줄바꿈(\\n): {actual_newlines}개")
    results.append(f"   - 리터럴 \\\\n: {literal_backslash_n}개")

    # 정규화 후 인증 테스트
    try:
        info = {k: v for k, v in raw.items() if k != "spreadsheet"}
        info["private_key"] = _normalize_private_key(info["private_key"])
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ]
        creds = Credentials.from_service_account_info(info, scopes=scopes)
        results.append("✅ Credentials 객체 생성 성공")
    except Exception as e:
        results.append(f"❌ Credentials 생성 실패: {e}")
        return results

    # 실제 API 호출 테스트
    try:
        import gspread
        client = gspread.authorize(creds)
        url = raw.get("spreadsheet", "")
        results.append(f"   - 시트 URL: {url[:60]}...")
        sh = client.open_by_url(url)
        results.append(f"✅ 시트 열기 성공: {sh.title}")
        ws = sh.worksheet("Sheet1")
        results.append(f"✅ Sheet1 열기 성공 (행 수: {ws.row_count})")
        # 실제 쓰기 테스트 (빈 행 추가 후 삭제)
        test_row = ["__test__", "__test__", 0, "__test__"]
        ws.append_row(test_row, value_input_option="USER_ENTERED")
        results.append("✅ 쓰기 테스트 성공!")
        # 테스트 행 삭제
        all_vals = ws.col_values(1)
        for idx, val in enumerate(reversed(all_vals), 1):
            if val == "__test__":
                ws.delete_rows(len(all_vals) - idx + 1)
                break
        results.append("✅ 테스트 행 정리 완료")
    except ImportError:
        results.append("⚠️ gspread 미설치 (requirements.txt 확인)")
    except Exception as e:
        results.append(f"❌ API 테스트 실패: {e}")

    return results


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
