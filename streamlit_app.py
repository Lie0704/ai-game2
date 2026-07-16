import random
import streamlit as st

WORD_BANK = [
    ("apple", "사과"),
    ("banana", "바나나"),
    ("school", "학교"),
    ("friend", "친구"),
    ("travel", "여행"),
    ("river", "강"),
    ("library", "도서관"),
    ("happy", "행복한"),
    ("music", "음악"),
    ("ocean", "바다"),
    ("weather", "날씨"),
    ("courage", "용기"),
]


def build_questions():
    questions = []
    for word, meaning in WORD_BANK:
        distractors = [korean for candidate_word, korean in WORD_BANK if candidate_word != word]
        options = [meaning] + random.sample(distractors, 3)
        random.shuffle(options)
        questions.append(
            {
                "word": word,
                "meaning": meaning,
                "options": options,
                "answer": meaning,
            }
        )
    return questions


def reset_game():
    st.session_state.questions = build_questions()
    st.session_state.current_index = 0
    st.session_state.score = 0
    st.session_state.show_answer = False
    st.session_state.choice = None


if "questions" not in st.session_state:
    reset_game()

questions = st.session_state.questions
current_index = st.session_state.current_index

st.set_page_config(page_title="영단어 게임", page_icon="📚", layout="centered")
st.title("📚 중학생 영단어 게임")
st.write("영단어의 뜻을 고르고, 정답을 맞혀보세요!")

if st.button("새 게임 시작", use_container_width=True):
    reset_game()
    st.rerun()

if current_index < len(questions):
    question = questions[current_index]

    st.progress((current_index + 1) / len(questions))
    st.write(f"문제 {current_index + 1}/{len(questions)}")
    st.write(f"단어: **{question['word']}**")

    selected = st.radio("뜻을 고르세요", question["options"], key="choice", index=None)

    if not st.session_state.show_answer:
        if st.button("정답 확인", use_container_width=True):
            if selected is None:
                st.warning("선택지를 골라주세요.")
            else:
                st.session_state.show_answer = True
                if selected == question["answer"]:
                    st.session_state.score += 1
                    st.success("정답입니다! 🎉")
                else:
                    st.error(f"아쉽네요. 정답은 {question['answer']}입니다.")
                st.info(f"이 단어의 뜻: {question['answer']}")
    else:
        if st.button("다음 문제", use_container_width=True):
            if current_index + 1 < len(questions):
                st.session_state.current_index += 1
                st.session_state.show_answer = False
                st.session_state.choice = None
                st.rerun()
            else:
                st.session_state.current_index = len(questions)
                st.rerun()

    st.caption(f"현재 점수: {st.session_state.score}/{current_index + 1}")
else:
    st.balloons()
    st.success(f"게임이 끝났어요! 총 {st.session_state.score}문제를 맞혔습니다.")
    st.write("다시 시작해 보세요!")
    if st.button("다시 시작", use_container_width=True):
        reset_game()
        st.rerun()
