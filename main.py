import streamlit as st

from app import show_eda
from Prediction import show_prediction

st.set_page_config(
    page_title="FraudShield AI",
    page_icon="🛡️",
    layout="wide"
)

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Go to",
    ["EDA Dashboard", "Fraud Prediction"]
)

if page == "EDA Dashboard":
    show_eda()

elif page == "Fraud Prediction":
    show_prediction()