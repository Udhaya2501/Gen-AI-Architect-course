import streamlit as st 
import random
import time

st.title("🧠 Timed Quiz App")

# -----------------------------
# Questions
# -----------------------------
questions = [
    {
        "question": "What is the capital of France?",
        "options": ["London", "Berlin", "Paris", "Rome"],
        "answer": "Paris"
    },
    {
        "question": "What is 5 + 3?",
        "options": ["5", "8", "10", "15"],
        "answer": "8"
    },
    {
        "question": "Which language is used for web apps?",
        "options": ["Python", "Java", "HTML", "All of the above"],
        "answer": "All of the above"
    }
]

# -----------------------------
# Session State Setup
# -----------------------------
if "start_time" not in st.session_state:
    st.session_state.start_time = None

if "shuffled_questions" not in st.session_state:
    st.session_state.shuffled_questions = None

# -----------------------------
# Start Quiz Button
# -----------------------------
if st.session_state.start_time is None:
    if st.button("Start Quiz"):
        st.session_state.start_time = time.time()
        st.session_state.shuffled_questions = random.sample(questions, len(questions))
        st.rerun()
else:
    # -----------------------------
    # Timer Logic (30 seconds)
    # -----------------------------
    time_limit = 30
    elapsed_time = int(time.time() - st.session_state.start_time)
    remaining_time = time_limit - elapsed_time

    if remaining_time <= 0:
        st.error("⏰ Time's up!")
        st.session_state.start_time = None
        st.stop()

    # -----------------------------
    # Status Bar
    # -----------------------------
    progress = st.progress(0)  # initialize progress bar
    progress_percent = int((elapsed_time / time_limit) * 100)
    progress.progress(progress_percent)
    st.warning(f"⏳ Time Remaining: {remaining_time} seconds")

    # -----------------------------
    # Show Questions
    # -----------------------------
    score = 0

    for i, q in enumerate(st.session_state.shuffled_questions):
        st.subheader(f"Question {i+1}")
        answer = st.radio(q["question"], q["options"], key=i)

        if answer == q["answer"]:
            score += 1

    # -----------------------------
    # Submit Button
    # -----------------------------
    if st.button("Submit"):
        st.success(f"Your score: {score}/{len(questions)}")

        if score == len(questions):
            st.balloons()

        # Reset quiz
        st.session_state.start_time = None