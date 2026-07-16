import random
import streamlit as st

st.set_page_config(page_title="영단어 & BTS", page_icon="🎵", layout="centered")

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
    st.session_state.pop("choice", None)


if "questions" not in st.session_state:
    reset_game()

questions = st.session_state.questions
current_index = st.session_state.current_index

st.title("📚 영어 공부 + BTS 소개")
st.write("영단어 게임도 하고, BTS도 알아보세요!")

word_tab, bts_tab = st.tabs(["📚 영단어 게임", "🎤 BTS 소개"])

with word_tab:
    st.header("영단어 게임")
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
                    st.session_state.pop("choice", None)
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

with bts_tab:
    st.header("BTS 소개")
    st.write("BTS는 방탄소년단으로, 한국의 대표적인 보이 그룹입니다.")
    st.write("멤버들은 노래, 춤, 그리고 진심 어린 메시지로 많은 사람들에게 사랑받고 있어요.")

    st.subheader("BTS의 특징")
    st.markdown(
        "- 멤버는 RM, Jin, Suga, J-Hope, Jimin, V, Jungkook입니다.\n"
        "- 음악과 춤을 모두 잘합니다.\n"
        "- 자기 자신을 사랑하라는 메시지를 많이 전합니다."
    )

    st.subheader("BTS가 유명한 이유")
    st.write("멋진 음악, 특별한 퍼포먼스, 그리고 팬들에게 따뜻한 인사를 전하기 때문입니다.")

    with st.expander("BTS 더 알아보기"):
        st.write("BTS는 세계적인 인기를 얻었고, 여러 나라에서 콘서트를 열었습니다.")
        st.write("그들의 노래는 영어와 한국어가 섞여 있어, 전 세계 사람들에게도 잘 알려져 있습니다.")
