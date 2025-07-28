import streamlit as st
# import datetime as dt

st.set_page_config(
    page_title='스마트 퀴즈',
    page_icon='💡',
    layout='centered'
)

#퀴즈 문제 데이터
quiz_questions = [
    {
        "type": "radio",
        "question": "다음 중 Streamlit에서 제목을 표시하는 함수는?",
        "options": ["st.title", "st.header", "st.subheader", "st.write"],
        "correct": 0,
        "explanation": "st.title()은 가장 큰 제목을 표시하는 함수입니다."
    },
    {
        "type": "text",
        "question": "Streamlit에서 텍스트를 입력받는 위젯은? (st.text_input에서 st. 제외하고 입력)",
        "correct": ["text_input"],
        "explanation": "st.text_input은 사용자로부터 텍스트를 입력받는 위젯입니다."
    },
    {
        "type": "slider",
        "question": "Streamlit 앱을 실행할 때 기본 포트 번호는?",
        "min_val": 8000,
        "max_val": 9000,
        "correct": 8501,
        "tolerance": 10,
        "explanation": "Streamlit 앱의 기본 포트는 8501번입니다."
    },
    {
        "type": "number",
        "question": "st.columns(3)을 사용하면 몇 개의 열이 생성되나요?",
        "correct": 3,
        "explanation": "st.columns(3)은 3개의 열을 생성합니다."
    },
    {
        "type": "selectbox",
        "question": "다음 중 Streamlit의 버튼 요소가 아닌 것은?",
        "options": ["st.button", "st.download_button", "st.slider", "st.form_submit_button"],
        "correct": 2,
        "explanation": "st.slider는 슬라이더 위젯이며 버튼 요소가 아닙니다."
    }
]

st.title('💡스마트 퀴즈')

st.write('Streamlit에 관한 퀴즈를 풀어보세요!')

if 'quiz_started' not in st.session_state:
    st.session_state.quiz_started = False

if 'answer_submitted' not in st.session_state:
    st.session_state.answer_submitted = False

if 'show_result' not in st.session_state:
    st.session_state.show_result = False

if 'quiz_finished' not in st.session_state:
    st.session_state.quiz_finished = False

if 'current_question' not in st.session_state:
    st.session_state.current_question = 0

if 'answers' not in st.session_state:
    st.session_state.answers = []

if 'is_correct' not in st.session_state:
    st.session_state.is_correct = None

if 'score' not in st.session_state:
    st.session_state.score = 0

def check_answer(question, user_answer):
    if question['type'] in ['radio', 'selectbox', 'slider', 'number']:
        return user_answer == question['correct']
    
    elif question['type'] == 'text':
        ans = ""
        for i in question['correct']:
            ans = i.lower()
        return user_answer in ans
    
    # if question['type'] == ['slider']:
        # return abs(user_answer - question['correct']) <= question['tolerance'] #abs는 절대값

    return False

if not st.session_state.quiz_started:
    st.header('📍퀴즈 소개')

    st.markdown("""
    - **총 문제 수**: 5문제
    - **문제 유형**: 객관식, 주관식, 슬라이더, 숫자 입력
    - **제한 시간**: 없음
    - **채점 방식**: 즉시 피드백
    """)

    st.info('준비되셨으면 아래 버튼을 눌러 퀴즈를 시작하세요.')

    col1, col2, col3 = st.columns(3)

    with col2:
        if st.button('퀴즈 시작', type='primary'):
            st.session_state.quiz_started = True
            st.session_state.answer_submitted = False
            st.session_state.show_result = False
            st.rerun()

    st.divider()

    st.subheader('❓문제 미리보기')

    for i, q in enumerate(quiz_questions):
        st.write(f'**문제{i+1}** : {q["question"]} ({q["type"]}유형)')

elif st.session_state.quiz_started and not st.session_state.quiz_finished:
    current_q=st.session_state.current_question
    question=quiz_questions[current_q]
    # prev_answer = st.session_state.answers.get(current_q)

    st.progress((current_q+1)/len(quiz_questions))

    st.subheader(f'문제{current_q+1}')
    st.write(question['question'])

    if not st.session_state.answer_submitted:
        user_answer=None

        if question['type'] == 'radio':
            user_answer = st.radio('보기'
                                   , options=range(len(question['options']))
                                   , format_func=lambda x : question['options'][x]
                                   , key=f'radio_{current_q}'
                                   , index=None
                                #    , index=prev_answer if prev_answer is not None else None
                                   )

        elif question['type'] == 'text':
            user_answer = st.text_input('입력란'
                                        , placeholder='정답을 입력하세요.'
                                        # , value=prev_answer if prev_answer else ''
                                        ).strip().lower()
            # st.write(user_answer)
        
        elif question['type'] == 'slider':
            user_answer = st.slider('슬라이드를 옮겨 정답을 선택하세요.'
                                    , min_value=question['min_val']
                                    , max_value=question['max_val']
                                    , value=(question['max_val']+question['min_val'])//2
                                    # , value=prev_answer if prev_answer is not None
                                    #   else (question['max_val']+question['min_val'])//2
                                    , key=f'slider_{current_q}'
                                    )
        
        elif question['type'] == 'number':
            user_answer = st.number_input('숫자를 입력하세요.'
                                          , step=1
                                        #   , value=prev_answer if prev_answer is not None else 0
                                          , key=f'number_{current_q}'
                                          )
            
        elif question['type'] == 'selectbox':
            user_answer = st.selectbox('보기'
                                       , options=range(len(question['options']))
                                       , format_func=lambda x : question['options'][x]
                                       , key=f'selectbox_{current_q}'
                                       , placeholder='정답을 선택하세요.'
                                       , index=None
                                    #    , index=prev_answer if prev_answer is not None else None
                                       )
            
        # st.divider()

        # col1, col2, col3, col4 = st.columns(4)
        col1, col2, col3 = st.columns(3)

        with col2:
            if st.button("답안 제출", type='primary'):
                #문제의 type이 text인 경우 빈 입력값 제출 시
                #st.warning 이용해 답을 입력하라고 출력
                if question['type'] == 'text' and not user_answer:
                    st.warning('답을 입력해주세요.')
                elif question['type'] in ['radio', 'selectbox'] and user_answer is None:
                    st.warning('답을 선택해주세요.')

                else:
                    is_correct = check_answer(question, user_answer)

                    # st.session_state.answers[current_q] = user_answer

                    st.session_state.answers.append({
                        'question':question['question'],
                        'user_answer':user_answer,
                        'correct_answer':question['correct'],
                        'is_correct':is_correct,
                        'explanation':question['explanation']
                    })

                    if is_correct:
                        st.session_state.score+=1

                    # st.session_state.is_correct=check_answer(question, user_answer)
                    st.session_state.answer_submitted=True
                    st.session_state.show_result=True
                    st.rerun()

        # with col3:
        #     if current_q > 0:
        #         if st.button('이전 문제'):
        #             st.session_state.current_question-=1
        #             st.session_state.answer_submitted=False
        #             st.session_state.show_result=False
        #             st.rerun()

    elif st.session_state.show_result:
        last_answer=st.session_state.answers[-1]

        if last_answer['is_correct']:
            st.success('정답입니다.')

        else:
            st.error('오답입니다.')

        st.info(f"해설:{last_answer['explanation']}")

        # st.divider()

    # else:
        # st.write(st.session_state.is_correct)
        # if st.session_state.is_correct:
        #     st.success('정답')
        # else:
        #     st.error('오답')

        # col1, col2, col3, col4 = st.columns(4)
        col1, col2, col3 = st.columns(3)
        
        with col2:
            if current_q < len(quiz_questions)-1:
                if st.button('다음 문제'):
                    st.session_state.current_question+=1
                    st.session_state.answer_submitted=False
                    st.session_state.show_result=False
                    st.rerun()

            else:
                if st.button('결과보기', type='primary'):
                    st.session_state.quiz_finished=True
                    st.rerun()

        # with col3:
        #     if current_q > 0:
        #         if st.button('이전 문제'):
        #             st.session_state.current_question-=1
        #             st.session_state.answer_submitted=False
        #             st.session_state.show_result=False
        #             st.rerun()

else:
    st.header('퀴즈 완료')

    total_questions=len(quiz_questions)
    score_percentage=(st.session_state.score/total_questions)*100

    def display_stat(title, value):
        st.markdown(f"""
            <div style="
                padding: 1rem; 
                background-color: var(--stat-bg, #f0f2f6); 
                border: 1px solid var(--stat-border, transparent);
                border-radius: 10px; 
                text-align: center;
                box-shadow: var(--stat-shadow, 0 1px 3px rgba(0,0,0,0.1));
            ">
                <div style="
                    font-size: 18px; 
                    font-weight: bold; 
                    color: var(--title-color, #262730);
                    margin-bottom: 0.5rem;
                ">{title}</div>
                <div style="
                    font-size: 32px; 
                    font-weight: bold; 
                    color: var(--text-color, #262730);
                ">{value}</div>
            </div>
            <br>
            <style>
                /* 라이트모드 기본값 */
                :root {{
                    --stat-bg: #f0f2f6;
                    --stat-border: transparent;
                    --stat-shadow: 0 1px 3px rgba(0,0,0,0.1);
                    --title-color: #262730;
                    --text-color: #262730;
                }}
                
                /* 다크모드 스타일 */
                @media (prefers-color-scheme: dark) {{
                    :root {{
                        --stat-bg: #2b2b35;
                        --stat-border: #404040;
                        --stat-shadow: 0 1px 3px rgba(0,0,0,0.3);
                        --title-color: #fafafa;
                        --text-color: #fafafa;
                    }}
                }}
                
                /* Streamlit 다크모드 */
                [data-theme="dark"] {{
                    --stat-bg: #2b2b35;
                    --stat-border: #404040;
                    --stat-shadow: 0 1px 3px rgba(0,0,0,0.3);
                    --title-color: #fafafa;
                    --text-color: #fafafa;
                }}
            </style>
        """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        display_stat('총 문제 수 : ', total_questions)
    with col2:
        display_stat('맞힌 문제 수 : ', st.session_state.score)
    with col3:
        display_stat('정답률 : ', f'{score_percentage:.1f}')

    if score_percentage == 100:
        st.success('모든 문제를 맞히셨습니다!')
    elif score_percentage >= 80:
        st.success('대부분의 문제를 맞히셨습니다.')
    elif score_percentage >= 60:
        st.info('반 이상의 문제를 맞히셨습니다.')
    else:
        st.error('아쉽습니다. 다시 도전해보세요!')

    st.divider()

    st.subheader('상세 결과')

    for i, answer in enumerate(st.session_state.answers):
        with st.expander(f'문제{i+1} : {"⭕"if answer["is_correct"] else "❌"}'):
            st.write(f'{answer["question"]}')

            if isinstance(answer['user_answer'], int) and 'options' in quiz_questions[i]:
                st.write(f'내 답 : {quiz_questions[i]["options"][answer["user_answer"]]}')
                st.write(f'정답 : {quiz_questions[i]["options"][answer["correct_answer"]]}')
            else:
                st.write(f'내 답 : {answer["user_answer"]}')
                if isinstance(answer['correct_answer'], list):
                    st.write(f'정답 : {", ".join(answer["correct_answer"])}')
                else:
                    st.write(f'정답 : {answer["correct_answer"]}')

            st.write('해설 : ', answer['explanation'])

    # st.divider()

    col1, col2, col3 = st.columns(3)

    with col2:
        if st.button('처음으로', type='primary'):
            st.session_state.quiz_started = False
            st.session_state.answer_submitted = False
            st.session_state.show_result = False
            st.session_state.quiz_finished = False
            st.session_state.current_question = 0
            st.session_state.answers = []
            st.session_state.is_correct = None
            st.session_state.score = 0
            st.rerun()

st.divider()

st.markdown(
    """
    <div style='text-align: center; color: gray; font-size: 0.8em; margin-top: 2rem;'>
    🧠 스마트 퀴즈 v1.1 | 다양한 문제 유형으로 지식을 테스트해보세요!
    </div>
    """,
    unsafe_allow_html=True
)