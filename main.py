import streamlit as st
from prompt_engine import build_prompt
from llm import generate_response
from utils import parse_response
from regression_model import (
    save_attempt,
    predict_next_accuracy,
    load_history,
    train_accuracy_models,
)

st.set_page_config(page_title="AI Tutor", layout="centered")

st.title("🎓 Personalized AI Tutor")

# --- User Inputs ---
topic = st.text_input("Enter Topic")

level = st.selectbox(
    "Select Level",
    ["Beginner", "Intermediate", "Advanced"]
)

num_questions = st.slider(
    "Number of quiz questions",
    min_value=3,
    max_value=15,
    value=5
)

# --- Generate Content ---
if st.button("Generate"):
    if topic.strip() == "":
        st.warning("Please enter a topic.")
    else:
        with st.spinner("Generating content..."):
            prompt = build_prompt(topic, level, num_questions)
            response = generate_response(prompt)
            data = parse_response(response)

        st.session_state["data"] = data
        st.session_state["topic"] = topic
        st.session_state["level"] = level
        st.session_state["num_questions"] = num_questions

        st.success("Content generated!")

# --- Display Results ---
if "data" in st.session_state:
    data = st.session_state["data"]

    tab1, tab2, tab3, tab4 = st.tabs(
        ["📘 Learning", "❓ Quiz", "💡 Explanation", "📊 Progress"]
    )

    # --- Learning Plan ---
    with tab1:
        st.subheader("Learning Plan")
        st.write(data["plan"])

    # --- Quiz ---
    with tab2:
        st.subheader("Quiz")

        questions = data["quiz"].split("\n\n")
        user_answers = []

        for i, q in enumerate(questions):
            if "Options" in q:
                parts = q.split("Options:")

                if len(parts) < 2:
                    continue

                question_text = parts[0]
                options = parts[1].split("\n")

                st.write(f"**Q{i + 1}: {question_text.strip()}**")

                options_clean = [
                    opt.strip()
                    for opt in options
                    if opt.strip()
                    and not opt.strip().startswith("Answer:")
                ]

                choice = st.radio(
                    f"Select answer {i + 1}",
                    options_clean,
                    key=f"question_{i}"
                )

                user_answers.append((choice, q))

        if st.button("Submit Quiz"):
            score = 0
            total = len(user_answers)

            for choice, q in user_answers:
                if "Answer:" in q:
                    correct = q.split("Answer:")[1].strip()

                    if correct and correct[0] in choice:
                        score += 1

            accuracy = score / total if total > 0 else 0

            st.success(f"Score: {score}/{total}")
            st.info(f"Current Accuracy: {accuracy * 100:.2f}%")

            save_attempt(
                st.session_state["topic"],
                st.session_state["level"],
                score,
                total
            )

            prediction_result = predict_next_accuracy(
                st.session_state["level"],
                score,
                total
            )

            if prediction_result:
                predicted_accuracy, model_name, results = prediction_result

                st.subheader("📈 Predicted Future Accuracy")
                st.write(f"Model Used: **{model_name}**")
                st.write(
                    f"Predicted Next Accuracy: **{predicted_accuracy * 100:.2f}%**"
                )

                st.subheader("Model Evaluation")

                for name, result in results.items():
                    st.write(f"**{name}**")
                    st.write(f"MAE: {result['mae']:.4f}")

                    if "mse" in result:
                        st.write(f"MSE: {result['mse']:.4f}")

                    st.write(f"R² Score: {result['r2']:.4f}")
            else:
                st.warning(
                    "Complete at least 5 quizzes to enable accuracy prediction."
                )

    # --- Explanation ---
    with tab3:
        st.subheader("Explanation")
        st.write(data["explanation"])

    # --- Progress ---
    with tab4:
        st.subheader("Student Progress History")

        history = load_history()

        if history.empty:
            st.info("No quiz history available yet.")
        else:
            st.dataframe(history)

            st.subheader("Accuracy Over Attempts")
            st.line_chart(history["accuracy"])