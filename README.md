# AI Personalized Tutor System

## Overview
AI Personalized Tutor is a Streamlit-based educational application that generates personalized learning plans, quiz questions, explanations, and student performance predictions.

The system uses an LLM through OpenRouter for content generation and regression models for predicting future student quiz accuracy.

## Features
- Personalized learning plan generation
- Topic-based quiz generation
- Interactive quiz answering
- Score and accuracy calculation
- Student progress tracking
- Regression-based future accuracy prediction
- Model evaluation using MAE, MSE, and R² score
- Docker-based deployment

## Technologies Used
- Python
- Streamlit
- OpenRouter API
- Pandas
- Scikit-learn
- Docker

## Project Structure
```text
aiapp/
├── main.py
├── llm.py
├── prompt_engine.py
├── utils.py
├── regression_model.py
├── requirements.txt
├── Dockerfile
├── README.md
├── .gitignore
└── .env
