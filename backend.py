# backend.py
import pandas as pd
from datetime import datetime
import streamlit as st

@st.cache_resource
def get_shared_db():
    """
    모든 세션이 공유하는 메모리 공간을 생성합니다.
    서버가 재시작되기 전까지 모든 학생의 데이터를 메모리에 보관합니다.
    """
    return {}

def login_student(student_id, name):
    db = get_shared_db()
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 학번을 키로 하여 정보 저장 또는 업데이트
    if student_id not in db:
        db[student_id] = {
            "student_id": student_id,
            "name": name,
            "last_login": now_str,
            "score": 0
        }
    else:
        # 기존 학번이 있으면 로그인 시간과 이름 업데이트
        db[student_id]["last_login"] = now_str
        db[student_id]["name"] = name

def update_score(student_id, new_score):
    db = get_shared_db()
    if student_id in db:
        # 기존 최고 점수보다 높을 때만 업데이트
        if new_score > db[student_id]["score"]:
            db[student_id]["score"] = new_score

def get_all_students():
    db = get_shared_db()
    if not db:
        return pd.DataFrame(columns=["학번", "이름", "퀴즈 점수", "마지막 접속"])
    
    # 딕셔너리 데이터를 리스트로 변환하여 Pandas DataFrame 생성
    data_list = []
    for s_id in db:
        data_list.append({
            "학번": db[s_id]["student_id"],
            "이름": db[s_id]["name"],
            "퀴즈 점수": db[s_id]["score"],
            "마지막 접속": db[s_id]["last_login"]
        })
    
    df = pd.DataFrame(data_list)
    
    # 마지막 접속 시간 기준 내림차순 정렬
    if not df.empty:
        df = df.sort_values(by="마지막 접속", ascending=False)
        
    return df
