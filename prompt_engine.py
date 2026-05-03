def build_prompt(topic, level, num_questions=5):
    return f"""
You are an AI tutor.

Student Level: {level}
Topic: {topic}

Respond STRICTLY in this format:

### Learning Plan
- Step 1:
- Step 2:
- Step 3:

### Quiz
Generate exactly {num_questions} multiple-choice questions.

For each question use this format:

1. Question: ...
   Options:
   A) ...
   B) ...
   C) ...
   D) ...
   Answer: A

### Explanation
Explain the topic simply.
"""