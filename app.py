# app.py
import streamlit as st
import time
import backend
from logic import tokenize, to_postfix, evaluate_postfix, check_quiz
from data import ARTICLES, QUIZ_QUESTIONS

def render_venn_svg(type, label_a="A", label_b="B"):
    # Base colors
    color_a = "#FF9999" # Reddish for Set A
    color_b = "#9999FF" # Blueish for Set B
    color_highlight = "#FFD700" # Yellow for highlights
    
    import uuid
    uid = str(uuid.uuid4())[:8]
    
    label_a = (label_a[:6] + '..') if len(label_a) > 7 else label_a
    label_b = (label_b[:6] + '..') if len(label_b) > 7 else label_b

    svg_header = f'<svg width="100%" height="150" viewBox="0 0 300 200" xmlns="http://www.w3.org/2000/svg" style="max-width:300px; display:block; margin:auto;">'
    
    if type == "and":
        content = f'''
            <circle cx="120" cy="100" r="80" fill="{color_a}" fill-opacity="0.2" stroke="#333" stroke-width="2"/>
            <circle cx="180" cy="100" r="80" fill="{color_b}" fill-opacity="0.2" stroke="#333" stroke-width="2"/>
            <clipPath id="clipAnd_{uid}">
                <circle cx="120" cy="100" r="80" />
            </clipPath>
            <circle cx="180" cy="100" r="80" fill="{color_highlight}" clip-path="url(#clipAnd_{uid})" fill-opacity="0.9" />
        '''
    elif type == "or":
        content = f'''
            <circle cx="120" cy="100" r="80" fill="{color_highlight}" fill-opacity="0.7" stroke="#333" stroke-width="2"/>
            <circle cx="180" cy="100" r="80" fill="{color_highlight}" fill-opacity="0.7" stroke="#333" stroke-width="2"/>
        '''
    elif type == "not":
        content = f'''
            <mask id="notMask_{uid}">
                <rect width="300" height="200" fill="white" />
                <circle cx="180" cy="100" r="80" fill="black" />
            </mask>
            <circle cx="180" cy="100" r="80" fill="{color_b}" fill-opacity="0.1" stroke="#333" stroke-width="2"/>
            <circle cx="120" cy="100" r="80" fill="{color_highlight}" mask="url(#notMask_{uid})" fill-opacity="0.9" stroke="#333" stroke-width="2"/>
        '''
    else: # type == "none" or keyword only
        content = f'''
            <circle cx="120" cy="100" r="80" fill="{color_highlight if type!='none' else color_a}" fill-opacity="0.5" stroke="#333" stroke-width="2"/>
            <circle cx="180" cy="100" r="80" fill="{color_b}" fill-opacity="0.1" stroke="#333" stroke-width="1" stroke-dasharray="4"/>
        '''

    text_content = ""
    
    return svg_header + content + text_content + "</svg>"


st.set_page_config(page_title="불리언 연산자 실습", page_icon="📚", layout="centered", initial_sidebar_state="collapsed")

# 로컬 스토리지처럼 사용될 세션 초기화
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.student_id = ""
    st.session_state.name = ""

if "quiz_current" not in st.session_state:
    st.session_state.quiz_current = 0
    st.session_state.quiz_score = 0
    st.session_state.quiz_answered = False

if "quiz_retry_count" not in st.session_state:
    st.session_state.quiz_retry_count = 0

if "menu_choice" not in st.session_state:
    st.session_state.menu_choice = "🎓 연구 과제 수행"

# ----------------- 로그인 페이지 -----------------
if not st.session_state.logged_in:
    st.title("📚 불리언 연산자 실습 접속")
    st.write("학생 조회를 위해 학번과 이름을 입력해주세요.")
    
    with st.form("login_form"):
        s_id = st.text_input("학번 (예: 20401, 관리자는 admin)")
        name = st.text_input("이름 (예: 홍길동)")
        submitted = st.form_submit_button("실습 시작", width="stretch")
        
        if submitted:
            if s_id and name:
                # DB 기록
                backend.login_student(s_id, name)
                
                st.session_state.logged_in = True
                st.session_state.student_id = s_id
                st.session_state.name = name
                st.rerun()
            else:
                st.error("학번과 이름을 모두 입력해야 합니다.")
    st.stop()


# ----------------- 모바일 친화적 상단 레이아웃 -----------------
# 타이틀 & 정보
col1, col2 = st.columns([7, 3])
with col1:
    st.markdown("### 📚 불리언 연산자 실습")
with col2:
    st.caption(f"👤 {st.session_state.student_id} {st.session_state.name}")
    if st.button("로그아웃", width="stretch"):
        st.session_state.logged_in = False
        st.rerun()

is_admin = (st.session_state.student_id == "admin") 

menu_options = ["🎓 연구 과제 수행", "📖 검색 연산자 가이드"]
if is_admin:
    menu_options.append("⚙️ 관리자 (Admin)")

# 상단을 탭처럼 사용하는 모바일 UI
choice = st.radio("메뉴이동", menu_options, horizontal=True, label_visibility="collapsed", key="menu_choice")
st.markdown("---")


# ----------------- 화면 1: 퀴즈 -----------------
if choice == "🎓 연구 과제 수행":
    st.title("연구 과제 수행 🎓")
    st.write("가상의 수행평가 및 학술 조사 시나리오를 읽고, 알맞은 검색식을 작성해보세요.")
    
    total_q = len(QUIZ_QUESTIONS)
    cur = st.session_state.quiz_current
    
    if cur >= total_q:
        st.success(f"🎉 모든 과제를 완수했습니다! 최종 점수: {st.session_state.quiz_score}/{total_q}")
        
        if "quiz_history" in st.session_state and st.session_state.quiz_history:
            st.markdown("### 📋 내 실습 결과 상세 분석표")
            import pandas as pd
            
            history_data = []
            for i, h in enumerate(st.session_state.quiz_history):
                history_data.append({
                    "문항": f"{i+1}번",
                    "입력한 검색식": h['answer'],
                    "검색 결과": f"{h.get('matched_count', 0)}건",
                    "정/오": "✅" if h['correct'] else "❌",
                    "상세 진단 피드백": h['feedback']
                })
            df_history = pd.DataFrame(history_data)
            st.dataframe(df_history, width="stretch", hide_index=True)

        if st.button("처음부터 다시 시작하기"):
            st.session_state.quiz_current = 0
            st.session_state.quiz_score = 0
            st.session_state.quiz_history = []
            st.session_state.quiz_retry_count = 0
            st.rerun()
    @st.fragment
    def quiz_area(cur, q):
        total_q = len(QUIZ_QUESTIONS)
        st.progress(cur / total_q)
        
        # 미션 카드 UI
        with st.container(border=True):
            st.caption(f"🏁 MISSION {cur+1}")
            st.markdown(f"### {q['question']}")
        
        # 실시간 논리 프리뷰 제거 (기존 127-140라인 삭제)
        
        st.write("")
        with st.form(key=f"quiz_form_{cur}", clear_on_submit=False):
            q_ans = st.text_input("검색식을 입력하고 Enter를 누르세요:", key=f"q_input_{cur}")
            submit_btn = st.form_submit_button("수행 결과 제출 ➡️", width="stretch", type="primary")

        if submit_btn:
            if not q_ans:
                st.warning("검색식을 입력해주세요!")
            else:
                from logic import get_logic_breakdown, check_quiz
                logic_data = get_logic_breakdown(q_ans)
                
                try:
                    is_correct, feedback = check_quiz(cur, q_ans)
                except Exception as e:
                    is_correct, feedback = False, f"문법 오류: 구조가 올바르지 않습니다."
                
                # 피드백 섹션 (벤다이어그램 포함)
                with st.status("🔍 제출된 논리 분석 중...", expanded=True) as status:
                    col_v, col_t = st.columns([4, 6])
                    with col_v:
                        k1 = logic_data['keywords'][0] if len(logic_data['keywords']) > 0 else "단어A"
                        k2 = logic_data['keywords'][1] if len(logic_data['keywords']) > 1 else "단어B"
                        st.markdown(render_venn_svg(logic_data['operator'].lower(), k1, k2), unsafe_allow_html=True)
                    with col_t:
                        st.info(f"**해석:** {logic_data['description']}")
                        if is_correct:
                            st.success(f"🎉 **정답입니다!** {feedback}")
                            status.update(label="✅ 분석 완료: 정답", state="complete", expanded=True)
                        else:
                            st.error(f"❌ **오답입니다:** {feedback}")
                            st.info(f"💡 **힌트:** {q['hint']}")
                            status.update(label="⚠️ 분석 완료: 오답", state="error", expanded=True)

                if is_correct:
                    if "quiz_history" not in st.session_state:
                        st.session_state.quiz_history = []
                    st.session_state.quiz_history.append({
                        "question": q['question'],
                        "answer": q_ans,
                        "correct": True,
                        "feedback": feedback,
                        "matched_count": 0,
                        "matched_titles": []
                    })
                    st.session_state.quiz_current += 1
                    st.session_state.quiz_score += 1
                    backend.update_score(st.session_state.student_id, st.session_state.quiz_score)
                    
                    st.info("ℹ️ 3초 후 다음 문제로 자동 이동합니다...")
                    time.sleep(3)
                    st.rerun()
                else:
                    if "quiz_history" not in st.session_state:
                        st.session_state.quiz_history = []
                    st.session_state.quiz_history.append({
                        "question": q['question'],
                        "answer": q_ans,
                        "correct": False,
                        "feedback": feedback,
                        "matched_count": 0,
                        "matched_titles": []
                    })
                    st.session_state.quiz_current += 1
                    
                    if st.button("기다리지 않고 다음 문제로 이동 ➡️", type="primary", width="stretch"):
                        st.rerun()
                    st.warning("⚠️ 5초 후 다음 문제로 자동 이동합니다...")
                    time.sleep(5)
                    st.rerun()

    if cur >= total_q:
        # (기존 결과 표시 로직)
        st.success(f"🎉 모든 과제를 완수했습니다! 최종 점수: {st.session_state.quiz_score}/{total_q}")
        # ... (생략된 내역) ...
    else:
        quiz_area(cur, QUIZ_QUESTIONS[cur])

# ----------------- 화면 3: 가이드 -----------------
elif choice == "📖 검색 연산자 가이드":
    st.title("전문 검색 엔진 연산자 가이드")
    
    # AND
    col1, col2 = st.columns([6, 4])
    with col1:
        st.markdown("""
        ### 🟩 AND (교집합)
        두 단어가 **모두** 포함된 건만 검색합니다. (검색 범위를 좁힘)
        - 예시: `기후 AND 정책`
        """)
    with col2:
        st.markdown(render_venn_svg("and"), unsafe_allow_html=True)
    
    # OR
    col1, col2 = st.columns([6, 4])
    with col1:
        st.markdown("""
        ### 🟦 OR (합집합)
        두 단어 중 **하나라도** 포함되면 검색합니다. (동의어 등 범위를 넓힘)
        - 예시: `저출산 OR 고령화`
        """)
    with col2:
        st.markdown(render_venn_svg("or"), unsafe_allow_html=True)
    
    # NOT
    col1, col2 = st.columns([6, 4])
    with col1:
        st.markdown("""
        ### 🟥 NOT (차집합)
        특정 단어가 들어간 문서를 **제외**합니다. (결과에서 원치 않는 내용 제거)
        - 예시: `지능 NOT 윤리`
        """)
    with col2:
        st.markdown(render_venn_svg("not"), unsafe_allow_html=True)
    
    st.markdown("""
    ---
    ### 🟪 ( ) (괄호 연산)
    묶은 부분의 **우선순위**를 지정합니다. 수학의 괄호와 같습니다.
    - 예시: `(딥페이크 OR 허위) AND 윤리`
    
    ### 🟧 " " (완전일치)
    글자 순서와 띄어쓰기까지 **정확히 일치**하는 단어만 검색합니다.
    - 예시: `"탄소 배출권"`
    """)

# ----------------- 화면 4: Admin -----------------
elif choice == "⚙️ 관리자 (Admin)":
    st.title("👨‍🏫 데이터베이스 관리 (Admin)")
    pwd = st.text_input("관리자 비밀번호를 입력하세요:", type="password")
    if pwd == "admin1234":
        st.success("인증 성공")
        
        df = backend.get_all_students()
        st.write("### 🎓 학생 접속 및 과제 수행 현황")
        st.dataframe(df, width="stretch")
        
        if not df.empty:
            avg_score = df["퀴즈 점수"].mean()
            st.metric("평균 퀴즈 점수", f"{avg_score:.1f} 점")
            
            csv = df.to_csv(index=False).encode('utf-8-sig')
            st.download_button(
                label="📥 액셀(CSV) 다운로드",
                data=csv,
                file_name='students_score.csv',
                mime='text/csv',
            )
            
    elif pwd != "":
        st.error("비밀번호가 틀렸습니다.")
