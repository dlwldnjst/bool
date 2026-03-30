import re
import streamlit as st

@st.cache_data
def tokenize(query):
    query = query.strip()
    if not query:
        return []
        
    tokens = []
    i = 0
    while i < len(query):
        if query[i].isspace():
            i += 1
            continue
            
        if query[i] == '(':
            tokens.append({"type": "LPAREN", "value": "("})
            i += 1
            continue
        if query[i] == ')':
            tokens.append({"type": "RPAREN", "value": ")"})
            i += 1
            continue
            
        if query[i] == '"':
            j = i + 1
            while j < len(query) and query[j] != '"':
                j += 1
            phrase = query[i+1:j].strip()
            if phrase:
                tokens.append({"type": "phrase", "value": phrase})
            # if missing closing quote, just consume to end
            i = j + 1
            continue
            
        # Read word
        j = i
        while j < len(query) and not query[j].isspace() and query[j] not in '()':
            # Stop if we hit a quote
            if query[j] == '"':
                break
            j += 1
            
        word = query[i:j].strip()
        if word:
            # 엄격한 대문자 검사 (사용자 요청: AND, OR, NOT은 대문자일 때만 파싱)
            if word == 'AND':
                tokens.append({"type": "AND", "value": "AND"})
            elif word == 'OR':
                tokens.append({"type": "OR", "value": "OR"})
            elif word == 'NOT':
                tokens.append({"type": "NOT", "value": "NOT"})
            else:
                tokens.append({"type": "term", "value": word})
        
        i = j
        
    return tokens

@st.cache_data
def to_postfix(tokens):
    processed = []
    # Add implicit ANDs
    for i, t in enumerate(tokens):
        processed.append(t)
        if i < len(tokens) - 1:
            next_t = tokens[i+1]
            is_end = t['type'] in ['term', 'phrase', 'RPAREN']
            is_start = next_t['type'] in ['term', 'phrase', 'LPAREN', 'NOT']
            if is_end and is_start:
                processed.append({"type": "AND", "value": "AND", "implicit": True})
                
    precedence = {'NOT': 3, 'AND': 2, 'OR': 1}
    output = []
    operators = []
    
    for t in processed:
        t_type = t['type']
        if t_type in ['term', 'phrase']:
            output.append(t)
        elif t_type == 'LPAREN':
            operators.append(t)
        elif t_type == 'RPAREN':
            while operators and operators[-1]['type'] != 'LPAREN':
                output.append(operators.pop())
            if operators and operators[-1]['type'] == 'LPAREN':
                operators.pop()
        elif t_type in precedence:
            while operators and operators[-1]['type'] != 'LPAREN' and \
                  precedence.get(operators[-1]['type'], 0) >= precedence[t_type]:
                output.append(operators.pop())
            operators.append(t)
            
    while operators:
        output.append(operators.pop())
        
    return {"originalTokens": processed, "postfix": output}

def evaluate_postfix(article, postfix):
    if not postfix:
        return True
        
    stack = []
    text = f"{article['title']} {article['excerpt']} {' '.join(article['tags'])}".lower()
    
    for t in postfix:
        if t['type'] in ['term']:
            stack.append(t['value'].lower() in text)
        elif t['type'] in ['phrase']:
            # Exact match logic (simple lowercase includes)
            stack.append(t['value'].lower() in text)
        elif t['type'] == 'AND':
            if len(stack) < 2: return False
            b = stack.pop()
            a = stack.pop()
            stack.append(a and b)
        elif t['type'] == 'OR':
            if len(stack) < 2: return False
            b = stack.pop()
            a = stack.pop()
            stack.append(a or b)
        elif t['type'] == 'NOT':
            if len(stack) < 2: return False
            b = stack.pop()
            a = stack.pop()
            stack.append(a and not b)
            
    return stack[0] if stack else False

def check_quiz(idx, q_input):
    """
    Validate quiz input using logic similar to JS app.
    Returns (True, "완전한 검색식입니다") if correct,
    False, "오답 사유 피드백" if wrong.
    """
    from data import QUIZ_QUESTIONS
    
    toks = tokenize(q_input)
    postfix_info = to_postfix(toks)
    ast = postfix_info['postfix']
    
    # 1. 일반 공통 에러: 소문자(and/or/not) 사용 여부 검사
    lower_ops = [t['value'] for t in toks if t['type'] == 'term' and t['value'] in ['and', 'or', 'not']]
    if lower_ops:
        return False, f"연산자는 반드시 대문자로 작성해야 합니다. (작성된 소문자: {', '.join(lower_ops)})"

    q_data = QUIZ_QUESTIONS[idx]
    if "validate" in q_data:
        return q_data["validate"](toks, ast)
        
    return False, "알 수 없는 오류"

@st.cache_data
def get_search_results(postfix):
    """
    Evaluates the AST postfix across all articles and returns matching ones.
    """
    from data import ARTICLES
    results = []
    for article in ARTICLES:
        # evaluate_postfix may throw if syntax is broken, but check_quiz handles it mostly
        try:
            if evaluate_postfix(article, postfix):
                results.append(article)
        except Exception:
            pass
    return results

@st.cache_data
def get_logic_breakdown(query):
    """
    Parses a query and returns a dictionary for UI preview:
    - keywords: list of words (A, B)
    - operator: 'AND', 'OR', 'NOT', or 'NONE'
    - description: Natural language translation
    """
    if not query:
        return {"keywords": [], "operator": "NONE", "description": "대기 중..."}
    
    try:
        from logic import tokenize, to_postfix
        tokens = tokenize(query)
        
        # Simple analysis for 2-word patterns
        keywords = [t['value'] for t in tokens if t['type'] not in ['AND', 'OR', 'NOT', 'LPAREN', 'RPAREN']]
        main_op = "NONE"
        for t in tokens:
            if t['type'] in ['AND', 'OR', 'NOT']:
                main_op = t['type']
                break
        
        desc = ""
        if main_op == "AND":
            desc = f"**'{keywords[0]}'**와 **'{keywords[1]}'** 기사가 **동시에** 포함된 결과를 찾습니다." if len(keywords) >= 2 else "두 키워드의 공통점을 찾습니다."
        elif main_op == "OR":
            desc = f"**'{keywords[0]}'** 또는 **'{keywords[1]}'** 중 하나라도 포함된 결과를 넓게 찾습니다." if len(keywords) >= 2 else "범위를 넓혀서 찾습니다."
        elif main_op == "NOT":
            desc = f"**'{keywords[0]}'** 내용 중 **'{keywords[1]}'**이 포함된 것은 제외하고 찾습니다." if len(keywords) >= 2 else "특정 내용을 제외하고 찾습니다."
        elif len(keywords) == 1:
            desc = f"키워드 **'{keywords[0]}'**만 포함된 결과를 정확히 찾습니다."
        else:
            desc = "복합적인 논리 구조를 분석 중입니다."
            
        return {"keywords": keywords[:2], "operator": main_op, "description": desc}
    except:
        return {"keywords": [], "operator": "NONE", "description": "수식 형식이 완벽하지 않습니다 (작성 중...)"}

