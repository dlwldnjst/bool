# data.py
import streamlit as st

@st.cache_data
def get_articles():
    return [
  # Science & Biology
  {
    "id": 1, "category": "science",
    "title": "크리스퍼(CRISPR) 유전자 가위의 원리와 최신 연구 동향",
    "excerpt": "CRISPR-Cas9 시스템을 이용한 유전자 교정에 대한 분자생물학적 원리와, 최신 오가노이드 모델에 적용된 연구 성과를 소개한다. 특히 오토파지와 연관된 난치성 질환 치료의 가능성을 조명한다.",
    "tags": ["CRISPR", "생명과학", "오가노이드", "유전자"],
    "date": "2026.01.12", "source": "생명과학연구", "url": "https://bio.example.com/crispr"
  },
  {
    "id": 2, "category": "science",
    "title": "양자컴퓨터의 오류 정정 기술과 알고리즘",
    "excerpt": "큐비트의 불안정성을 극복하기 위한 양자컴퓨터 오류 정정 기술의 현재와, 쇼어 알고리즘이 현대 암호체계에 미치는 파급력을 물리학적 관점에서 설명한다.",
    "tags": ["양자컴퓨터", "물리학", "알고리즘", "보안"],
    "date": "2025.11.08", "source": "응용물리학회지", "url": "https://phys.example.com/quantum"
  },
  {
    "id": 3, "category": "ethics",
    "title": "생명과학 발전과 생명 윤리: 유전자 교정 아기를 중심으로",
    "excerpt": "크리스퍼 기술을 인간 배아에 적용하는 문제에 대한 윤리적 딜레마. 칸트의 의무론적 관점과 공리주의적 관점에서 유전자 교정을 통한 향상(enhancement)이 정당한가에 대해 논의함.",
    "tags": ["윤리", "생명윤리", "CRISPR", "칸트", "의무론"],
    "date": "2025.07.24", "source": "철학과윤리", "url": "https://eth.example.org/gene"
  },
  {
    "id": 4, "category": "environment",
    "title": "엘니뇨 현상과 해수면 온도 변화가 글로벌 기후에 미치는 영향",
    "excerpt": "적도 태평양의 해수면 온도 상승(엘니뇨)이 유발하는 이상 기후 메커니즘을 분석하고, 지구 온난화가 해당 주기에 미치는 영향을 다기능 기후 모델을 통해 살펴본다.",
    "tags": ["기후", "지구과학", "엘니뇨", "온난화"],
    "date": "2026.02.15", "source": "지구과학회지", "url": "https://earth.example.org/elnino"
  },
  {
    "id": 5, "category": "tech",
    "title": "인공지능과 알고리즘이 만드는 필터 버블 현상",
    "excerpt": "소셜 미디어의 추천 알고리즘이 사용자에게 확증 편향을 강화하는 '필터 버블' 현상의 정보학적 메커니즘을 분석하고, 정보 민주주의에 미치는 악영향을 경고한다.",
    "tags": ["인공지능", "필터 버블", "알고리즘", "정보사회"],
    "date": "2025.09.30", "source": "디지털사회연구", "url": "https://tech.example.net/filter-bubble"
  },
  {
    "id": 6, "category": "environment",
    "title": "탄소국경조정제도(CBAM)의 도입이 무역 경제에 미치는 영향",
    "excerpt": "EU가 주도하는 탄소국경조정제도(CBAM)의 원리를 경제학적으로 분석하고, 탄소 배출권 거래제와 연계하여 수출 중심형 국가들의 정책적 전환 필요성을 역설한다.",
    "tags": ["CBAM", "탄소 배출권", "경제", "정책", "기후"],
    "date": "2026.03.05", "source": "경제정책리뷰", "url": "https://econ.example.com/cbam"
  },
  {
    "id": 7, "category": "ethics",
    "title": "칸트의 의무론과 벤담의 공리주의: 현대 사회의 도덕적 딜레마",
    "excerpt": "자율주행 자동차의 사고 알고리즘 트롤리 딜레마를 중심으로, 칸트의 보편적 의무론과 벤담의 양적 공리주의 중 무엇이 더 적합한 윤리적 기준을 제시하는가 비교 연구.",
    "tags": ["칸트", "의무론", "공리주의", "윤리", "철학"],
    "date": "2025.04.11", "source": "현대철학연구", "url": "https://phil.example.kr/kant"
  },
  {
    "id": 8, "category": "society",
    "title": "저출산 고령화 사회의 진입과 복지 정책의 구조적 개편",
    "excerpt": "한국의 저출산 및 고령화 지표 변화 양상을 통계적으로 분석하고, 생산가능인구 감소에 따른 국민연금 및 복지 정책 개편 방안을 제언한다.",
    "tags": ["저출산", "고령화", "복지", "정책", "사회"],
    "date": "2026.01.29", "source": "사회학논총", "url": "https://soc.example.kr/demo"
  },
  {
    "id": 9, "category": "environment",
    "title": "도시 생물 다양성 보존을 위한 비오톱(Biotope) 조성 연구",
    "excerpt": "무분별한 도시 개발 속에서 생물 다양성을 유지하기 위한 구체적 대안으로서 비오톱 네트워크 정책의 실효성을 생태학적 관점에서 점검한다.",
    "tags": ["생물 다양성", "비오톱", "도시", "환경", "동식물", "생태계"],
    "date": "2025.05.22", "source": "도시환경연구", "url": "https://city.example.com/bio"
  },
  {
    "id": 10, "category": "society",
    "title": "글로벌 인플레이션 장기화와 각국 중앙은행의 기준 금리 인상",
    "excerpt": "코로나19 팬데믹 이후 발생한 공급망 교란과 인플레이션 현상을 분석하고, 물가 안정을 위한 금리 인상 정책이 가계 부채 및 경제에 미치는 부작용을 고찰한다.",
    "tags": ["인플레이션", "금리", "경제", "거시경제", "정책"],
    "date": "2025.10.12", "source": "재무금융연구", "url": "https://fin.example.com/inflation"
  },
  {
    "id": 11, "category": "society",
    "title": "부동산 시장 안정화를 위한 조세 정책의 한계와 과제",
    "excerpt": "최근 10년간 도입된 각종 부동산 조세 및 대출 규제 정책이 시장 가격에 미친 영향을 회귀분석하여 조세 전가 현상을 실증적으로 규명한다.",
    "tags": ["부동산", "조세", "경제", "정책"],
    "date": "2025.08.30", "source": "부동산경제학", "url": "https://realestate.example.com/tax"
  },
  {
    "id": 12, "category": "tech",
    "title": "딥페이크(Deepfake) 기술의 악용 사례와 기술적 탐지 방안",
    "excerpt": "적대적 생성 신경망(GAN)을 활용한 딥페이크 기술의 발전이 초래하는 허위 조작 정보의 심각성과 이를 인공지능으로 다시 판별해내는 탐지 알고리즘 기술 동향.",
    "tags": ["딥페이크", "인공지능", "허위 조작", "보안", "미디어"],
    "date": "2026.02.20", "source": "차세대컴퓨팅", "url": "https://ai.example.org/deepfake"
  },
  {
    "id": 13, "category": "ethics",
    "title": "생성형 AI의 저작권 무단 학습과 창작 윤리 논쟁",
    "excerpt": "인공지능이 인간의 창작물을 허락 없이 학습 데이터로 사용하는 것이 가지는 법적, 윤리적 문제점을 지적하며, '공정 이용'의 한계에 대해 논한다.",
    "tags": ["인공지능", "윤리", "저작권", "법학"],
    "date": "2025.12.05", "source": "법학논집", "url": "https://law.example.kr/ai-ethics"
  },
  {
    "id": 14, "category": "environment",
    "title": "해양 생태계를 파괴하는 미세플라스틱의 흡착 기작 연구",
    "excerpt": "미세플라스틱이 해양으로 유입된 후 중금속 및 독성 물질을표면에 흡착하여 해양 생물의 체내에 축적되는 물리화학적 기작을 분석한다.",
    "tags": ["플라스틱", "미세플라스틱", "해양", "환경", "오염"],
    "date": "2025.06.18", "source": "해양과학회지", "url": "https://ocean.example.com/microplastic"
  },
  {
    "id": 15, "category": "environment",
    "title": "폐플라스틱 열분해를 통한 화학적 재활용 기술 동향",
    "excerpt": "기존 물리적 재활용의 한계를 극복하기 위해 플라스틱을 고열로 분해하여 원료 상태로 되돌리는 화학적 재활용 기술의 경제성과 환경적 실효성을 점검한다.",
    "tags": ["플라스틱", "재활용", "화학", "환경"],
    "date": "2026.01.07", "source": "화학공학연구", "url": "https://chem.example.kr/plastic-recycle"
  },
  {
    "id": 16, "category": "history",
    "title": "3·1 운동의 도화선이 된 민족 자결주의와 2.8 독립 선언",
    "excerpt": "1919년 3·1 운동이 발발하기까지 윌슨의 민족 자결주의 제창과 도쿄 유학생들의 2.8 독립 선언이 미친 사상적 맥락을 역사학적으로 추적한다.",
    "tags": ["3·1 운동", "독립운동", "근현대사", "역사", "조선"],
    "date": "2026.02.28", "source": "역사비평", "url": "https://hist.example.org/1919"
  },
  {
    "id": 17, "category": "history",
    "title": "대한민국 임시정부의 수립과 외교 독립노선의 전개",
    "excerpt": "상하이 대한민국 임시정부의 외교주의 노선 성공과 한계, 그리고 이승만, 김구 등의 파벌 간 이념적 차이가 독립운동의 방향에 미친 영향을 분석함.",
    "tags": ["임시정부", "독립운동", "외교", "근현대사", "역사"],
    "date": "2025.08.15", "source": "한국사학보", "url": "https://hist.example.org/kpg"
  },
  {
    "id": 18, "category": "history",
    "title": "갑오개혁이 조선 봉건 신분제 철폐에 미친 파급 효과",
    "excerpt": "1894년 반포된 갑오개혁 문서들을 바탕으로, 법제적인 신분 해방이 실제 평민과 노비 계층의 삶과 경제적 토대에 어떤 실질적 변화를 가져왔는지 고찰한다.",
    "tags": ["갑오개혁", "근현대사", "신분제", "역사", "조선"],
    "date": "2025.11.20", "source": "역사교육포럼", "url": "https://edu-history.example.kr/1894"
  },
  {
    "id": 19, "category": "tech",
    "title": "클라우드 컴퓨팅 환경에서의 데이터 암호화 프로토콜 안전성",
    "excerpt": "프라이빗 클라우드 환경에서 저장 및 전송되는 데이터를 보호하기 위한 최신 동형 암호 체계의 연산 속도와 안전성을 벤치마킹하여 성능을 평가함.",
    "tags": ["클라우드", "데이터", "보안", "암호화", "컴퓨터공학"],
    "date": "2026.03.11", "source": "정보보호학회", "url": "https://tech.example.org/cloud-sec"
  },
  {
    "id": 20, "category": "society",
    "title": "무한경쟁 사회의 교육 격차와 사교육 의존도 심화 원인",
    "excerpt": "대학 입시 위주의 교육 스키마가 야기하는 사회 경제적 계층에 따른 교육 격차 현상을 지니계수 및 소득 분위를 통해 통계적으로 실증한다.",
    "tags": ["교육", "격차", "사회학", "통계", "사교육"],
    "date": "2025.09.05", "source": "한국사회현상", "url": "https://soc.example.kr/edu-gap"
  },
  {
    "id": 21, "category": "science",
    "title": "세포 자멸사(Apoptosis)의 분자 모델링과 항암 치료제 개발",
    "excerpt": "오작동하는 세포의 자연 사멸(Apoptosis)을 유도하는 단백질 수용체를 표적으로 삼는 신규 항암 화합물의 IN-VITRO 실험 결과를 분석함.",
    "tags": ["세포", "항암", "생명과학", "의학", "분자생물학"],
    "date": "2025.12.22", "source": "생의학연구", "url": "https://bio.example.com/apoptosis"
  },
  {
    "id": 22, "category": "ethics",
    "title": "안락사 합법화에 대한 존엄사 인정 요건과 생명 윤리",
    "excerpt": "인간다운 죽음을 맞이할 권리(존엄사)와 생명 절대 존중 사상 사이의 윤리적 충돌을 스위스의 디그니타스 사례와 비교법적으로 분석한다.",
    "tags": ["윤리", "생명윤리", "안락사", "사망예방", "법학"],
    "date": "2026.01.05", "source": "생명법학회", "url": "https://eth.example.org/euthanasia"
  },
  {
    "id": 23, "category": "tech",
    "title": "블록체인 분산 원장 기술을 활용한 무결성 검증 아키텍처",
    "excerpt": "기존 중앙 집중형 데이터베이스의 보안 취약점을 극복하기 위해 하이퍼레저 패브릭을 접목한 분산 원장 데이터 무결성 검증 속도를 개선하는 논문.",
    "tags": ["블록체인", "데이터", "무결성", "보안", "암호화"],
    "date": "2025.03.15", "source": "분산원장논문지", "url": "https://tech.example.com/blockchain"
  },
  {
    "id": 24, "category": "environment",
    "title": "대기 중 초미세먼지(PM2.5)가 호흡기 질환 유발에 미치는 역학적 연구",
    "excerpt": "국내 주요 대도시 10년치 대기 질 데이터와 국민건강보험공단 심평원 데이터를 결합 분석하여 초미세먼지 농도와 호흡기 질환 발병률 간의 인과성을 증명함.",
    "tags": ["미세먼지", "환경", "기후", "역학", "건강"],
    "date": "2025.07.01", "source": "보건환경학", "url": "https://env.example.org/pm25"
  }
]

ARTICLES = get_articles()


def has_type(arr, typ):
    return any(x['type'] == typ for x in arr)

def has_val(arr, val):
    val = val.lower()
    return any(x.get('value', '').lower() == val for x in arr)

def q0_validate(toks, ast):
    if not has_type(toks, 'AND'): return False, "묵시적 AND(띄어쓰기)가 아닌 명시적인 AND 연산자를 입력해야 합니다."
    if has_type(toks, 'NOT') or has_type(toks, 'OR'): return False, "이 문항에서는 NOT이나 OR 대신 AND 연산자만 필요합니다."
    if not (has_val(ast, '칸트') and has_val(ast, '의무론')): return False, "필수 키워드('칸트', '의무론')가 누락되었거나 오타가 있습니다."
    return True, "정답! AND 연산자의 올바른 사용입니다."

def q1_validate(toks, ast):
    if not has_type(ast, 'phrase'): return False, '따옴표(" ")를 사용한 완전일치 검색 구문이 누락되었습니다.'
    if not any(x['type'] == 'phrase' and x['value'] == '필터 버블' for x in ast): return False, "필터 버블 이라는 단어가 정확히 따옴표 안에 들어가야 합니다."
    return True, "정답! 완전일치 구문 검색을 정확히 이해했습니다."

def q2_validate(toks, ast):
    if not has_type(toks, 'NOT'): return False, "제외할 단어 앞에는 NOT 연산자가 필수적입니다."
    if has_type(toks, 'OR') or has_type(toks, 'AND'): return False, "이 문항에서는 특정 단어를 제외(NOT)하는 로직만 구성해보세요."
    if not ((has_val(ast, 'crispr') or has_val(ast, 'cr')) and has_val(ast, '윤리')): return False, "주제어(CRISPR)와 제외어(윤리)가 올바르게 입력되지 않았습니다."
    return True, "정답! NOT 연산자로 불필요한 데이터를 잘 걸러냈습니다."

def q3_validate(toks, ast):
    if not has_type(toks, 'OR'): return False, "두 개념 중 하나라도 포함시키려면 OR 연산자를 써야 합니다."
    if has_type(toks, 'NOT'): return False, "제외할 조건이 없는데 NOT 연산자가 사용되었습니다."
    if not (has_val(ast, '저출산') and has_val(ast, '고령화')): return False, "'저출산', '고령화' 키워드가 누락되었습니다."
    return True, "정답! OR 연산자로 검색 스펙트럼을 훌륭히 넓혔습니다."

def q4_validate(toks, ast):
    if not (has_type(toks, 'AND') and has_type(toks, 'NOT')): return False, "AND 연산자와 NOT 연산자가 모두 1번 이상 포함되어야 합니다."
    if not (has_val(ast, '인플레이션') and has_val(ast, '금리') and has_val(ast, '부동산')): return False, "주어진 3개의 키워드를 모두 식에 포함시켜야 합니다."
    return True, "정답! 복합 논리를 안정적으로 작성했습니다."

def q5_validate(toks, ast):
    if not has_type(toks, 'LPAREN'): return False, "연산자 우선순위를 명확히 하기 위해 괄호 '( )'가 필요합니다."
    if not (has_type(toks, 'OR') and has_type(toks, 'AND')): return False, "OR와 AND 연산자가 결합되어야 합니다."
    if not (has_val(ast, '딥페이크') and has_val(ast, '윤리')): return False, "핵심 단어(딥페이크, 윤리)가 누락되었습니다."
    return True, "정답! 괄호의 우선순위를 정확하게 묶었습니다."

def q6_validate(toks, ast):
    if not has_type(ast, 'OR'): return False, "유사한 두 개념(임시정부, 독립운동)은 OR 연산자로 묶어야 합니다."
    if not any(x['type'] == 'phrase' and '3·1 운동' in x['value'] for x in ast): return False, "3·1 운동 은 띄어쓰기까지 일치하도록 따옴표로 감싸야 기합니다."
    if not (has_val(ast, '임시정부') or has_val(ast, '독립운동')): return False, "임시정부 또는 독립운동 단어가 포함되어야 합니다."
    return True, "정답! 괄호, OR, AND, 따옴표가 모두 결합된 고급 검색식입니다."

def q7_validate(toks, ast):
    if not has_type(toks, 'LPAREN'): return False, "우선적으로 처리할 단어 묶음에 괄호 '(' 가 없습니다."
    if not (has_type(toks, 'OR') and has_type(toks, 'NOT')): return False, "OR 및 NOT 연산자가 포함되지 않았습니다."
    if not (has_val(ast, '플라스틱') and has_val(ast, '해양') and has_val(ast, '미세플라스틱')): return False, "네 가지 키워드(플라스틱, 온난화, 해양, 미세플라스틱) 중 누락이 있습니다."
    return True, "정답! 축하합니다. 가장 복잡한 보스전 검색식을 완벽히 해냈습니다!"

QUIZ_QUESTIONS = [
  {
    "type": "AND",
    "question": "[수행평가 1] 생활과 윤리 보고서 작성을 위해 :orange[**칸트**]와 :orange[**의무론**] 두 단어가 :red[**모두**] 포함된 학술 자료를 찾고자 합니다.",
    "hint": "두 핵심 키워드를 반드시 모두 포함시켜야 할 때는 AND 연산자를 사용합니다.",
    "example": "칸트 AND 의무론",
    "validate": q0_validate
  },
  {
    "type": "EXACT",
    "question": "[수행평가 2] 국어시간, :orange[**\"필터 버블\"**] 현상에 관한 논문을 찾고 싶습니다. 다른 뜻으로 파싱되는 걸 막기 위해 무조건 저 구문이 :red[**완전 일치**]해야 합니다.",
    "hint": "정확한 문구나 표현은 겹따옴표(\" \")로 묶어줍니다.",
    "example": "\"필터 버블\"",
    "validate": q1_validate
  },
  {
    "type": "NOT",
    "question": "[자료탐색 1] 생명과학 수업을 맞아 :orange[**CRISPR**]을 조사 중입니다. 단, :orange[**윤리**]적인 논란을 다룬 문서는 철저히 :red[**배제**]하고 순수 기술(과학) 문서만 찾으려 합니다.",
    "hint": "검색 노이즈를 줄이기 위해 제외할 단어 앞에 NOT 연산자를 배치하세요.",
    "example": "CRISPR NOT 윤리",
    "validate": q2_validate
  },
  {
    "type": "OR",
    "question": "[자료탐색 2] 저출산 혹은 고령화 문제와 관련된 통계를 찾습니다. :orange[**저출산**] :red[**또는**] :orange[**고령화**] 둘 중 하나라도 포함된 자료를 다 찾아보세요.",
    "hint": "검색 범위를 크게 확장할 때는 관련 동의어나 유사어 사이에 OR 연산자를 넣습니다.",
    "example": "저출산 OR 고령화",
    "validate": q3_validate
  },
  {
    "type": "MIX",
    "question": "[심화 1] 경제 동아리에서 :orange[**인플레이션**]과 :orange[**금리**]가 :red[**모두**] 언급된 기사를 찾되, :orange[**부동산**] 이야기 들어간 기사는 :red[**제외**]하려 합니다.",
    "hint": "AND와 NOT을 순서대로 조합하면 됩니다. 예: A AND B NOT C",
    "example": "인플레이션 AND 금리 NOT 부동산",
    "validate": q4_validate
  },
  {
    "type": "PAREN",
    "question": "[심화 2] IT 과제 조사: :orange[**딥페이크 또는 인공지능**] 중 하나를 다루면서, 반드시 :orange[**윤리**] 문제가 :red[**같이**] 언급된 기사 묶음을 검색하세요. 괄호()를 사용하여 묶어보세요.",
    "hint": "우선순위를 정할 때 수학처럼 괄호 연산자를 쓸 수 있습니다. 예: (A OR B) AND C",
    "example": "(딥페이크 OR 인공지능) AND 윤리",
    "validate": q5_validate
  },
  {
    "type": "MIX",
    "question": "[응용 1] 역사 수행평가: :orange[**임시정부**] :red[**또는**] :orange[**독립운동**]에 대한 글을 찾는데, :orange[**\"3.1 운동\"**]은 완전일치구문으로 무조건 함께 :red[**포함**]되어야 합니다.",
    "hint": "단어를 괄호로 묶고 OR을 쓴 뒤, 완전일치 조건을 AND로 결합하세요.",
    "example": "(임시정부 OR 독립운동) AND \"3·1 운동\"",
    "validate": q6_validate
  },
  {
    "type": "PAREN",
    "question": "[응용 2] :orange[**플라스틱**] :red[**또는**] :orange[**온난화**] 단어가 들어가고, 동시에 :orange[**해양**] 이 들어간 글을 찾되, :orange[**미세플라스틱**]은 :red[**제외**]하는 최고의 검색식을 작성해보세요.",
    "hint": "모든 연산자가 투입되는 보스전입니다! (A OR B) AND C NOT D 구조로 작성하세요.",
    "example": "(플라스틱 OR 온난화) AND 해양 NOT 미세플라스틱",
    "validate": q7_validate
  }
]
