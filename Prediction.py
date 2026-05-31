import streamlit as st
import pickle
import pandas as pd

def show_prediction():
    st.set_page_config(
        page_title="Fraud Detection System",
        page_icon="💳",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # =====================================
    # LOAD MODEL
    # =====================================

    with open('fraud_detection_model1.pkl', 'rb') as file:
        model = pickle.load(file)

    # =====================================
    # LOAD LABEL MAPPINGS
    # =====================================

    with open('label_mappings.pkl', 'rb') as file:
        label_mappings = pickle.load(file)

    # =====================================
    # LOAD FEATURE NAMES
    # =====================================

    with open('feature_names1.pkl', 'rb') as file:
        feature_names = pickle.load(file)

    # =====================================
    # CUSTOM CSS
    # =====================================

    st.markdown("""
    <style>

    /* Import Font */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

    /* Global Styling */
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }

    /* Main Background */
    .stApp {
        background: #1c1c1c;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        padding: 20px;
    }

    /* Title */
    .main-title {
        text-align: center;
        font-size: 3rem;
        font-weight: 700;
        color: #38bdf8;
        margin-bottom: 10px;
    }

    /* Subtitle */
    .subtitle {
        text-align: center;
        font-size: 1.1rem;
        color: #cbd5e1;
        margin-bottom: 35px;
    }

    /* Input Labels */
    label {
        color: white !important;
        font-weight: 500 !important;
    }

    /* Selectbox */
    .stSelectbox div[data-baseweb="select"] {
        background-color: #1e293b;
        border-radius: 12px;
    }

    /* Number Input */
    .stNumberInput input {
        background-color: #1e293b !important;
        color: white !important;
        border-radius: 10px !important;
    }

    /* Slider */
    .stSlider {
        padding-top: 10px;
        padding-bottom: 10px;
    }

    /* Predict Button */
    .stButton > button {

        width: 1165%;
        background: linear-gradient(135deg, #2563eb, #06b6d4);
        color: white;
        border: none;
        border-radius: 14px;
        padding: 14px;
        font-size: 18px;
        font-weight: 700;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }

    /* Button Hover Effect */
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 8px 25px rgba(0,0,0,0.2);
        background: #1D293D;
        color: yellow;
    }

    /* Success Box */
    div[data-testid="stSuccess"] {
        background-color: #052e16;
        border-radius: 15px;
        padding: 12px;
    }
            
    div[data-testid="stSuccess"]:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(34,197,94,0.25);
    }

    /* Error Box */
    div[data-testid="stError"] {
        background-color: #450a0a;
        border-radius: 15px;
        padding: 12px;
    }

    /* Warning Box */
    div[data-testid="stWarning"] {
        background-color: #3b2f00;
        border-radius: 15px;
        padding: 12px;
    }

    div[data-testid="stWarning"]:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(251,191,36,0.25);
    }
                
    /* ---------------------------------------------------
    FOOTER
    --------------------------------------------------- */
    .footer {

        text-align: center;
        margin-top: 1px;
        padding-top: 20px;
        color: #CAD5E2;
        font-size: 20px;
    }

    /* ---------------------------------------------------
    HIGHLIGHT TEXT
    --------------------------------------------------- */
    .highlight {

        color: #CAD5E2 !important;
        font-weight: bold;
        text-shadow: 0px 0px 10px rgba(144,161,185,0.3);
    }

    </style>
    """, unsafe_allow_html=True)

    # =====================================
    # PAGE TITLE
    # =====================================

    st.markdown(
        """
        <h1 class="main-title">
            💳 Fraud Detection System
        </h1>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <p class="subtitle">
            AI-Powered Transaction Fraud Analysis Dashboard
        </p>
        """,
        unsafe_allow_html=True
    )

    # =====================================
    # USER INPUTS
    # =====================================

    transaction_amount = st.number_input(
        "Transaction Amount",
        min_value=0.0
    )

    merchant_category = st.selectbox(
        "Merchant Category",
        list(label_mappings['Merchant_Category'].keys())
    )

    payment_method = st.selectbox(
        "Payment Method",
        list(label_mappings['Payment_Method'].keys())
    )

    device_type = st.selectbox(
        "Device Type",
        list(label_mappings['Device_Type'].keys())
    )

    location = st.selectbox(
        "Location",
        list(label_mappings['Location'].keys())
    )

    is_international = st.selectbox(
        "International Transaction",
        [0, 1]
    )

    previous_transactions = st.number_input(
        "Previous Transactions",
        min_value=0
    )

    average_spend = st.number_input(
        "Average Spend",
        min_value=0.0
    )

    account_age_days = st.number_input(
        "Account Age (Days)",
        min_value=0
    )

    suspicious_keyword = st.selectbox(
        "Suspicious Keyword",
        list(label_mappings['Suspicious_Keyword'].keys())
    )

    month = st.slider(
        "Month",
        1,
        12
    )

    weekday = st.slider(
        "Weekday",
        0,
        6
    )

    # =====================================
    # FEATURE ENGINEERING
    # =====================================

    is_weekend = 1 if weekday in [5, 6] else 0

    spend_deviation = (
        transaction_amount - average_spend
    )

    spend_ratio = (
        transaction_amount / (average_spend + 1)
    )

    high_value_transaction = (
        1 if transaction_amount > 10000 else 0
    )

    customer_activity_score = (
        previous_transactions + average_spend
    )

    transactions_per_day = (
        previous_transactions /
        (account_age_days + 1)
    )

    # =====================================
    # PREDICTION BUTTON
    # =====================================

    if st.button("Predict Fraud"):

        # =====================================
        # ENCODE CATEGORICAL FEATURES
        # =====================================

        merchant_category = label_mappings[
            'Merchant_Category'
        ][merchant_category]

        payment_method = label_mappings[
            'Payment_Method'
        ][payment_method]

        device_type = label_mappings[
            'Device_Type'
        ][device_type]

        location = label_mappings[
            'Location'
        ][location]

        suspicious_keyword = label_mappings[
            'Suspicious_Keyword'
        ][suspicious_keyword]

        # =====================================
        # CREATE INPUT DATA
        # =====================================

        input_data = {

            'Transaction_Amount': transaction_amount,

            'Merchant_Category': merchant_category,

            'Payment_Method': payment_method,

            'Device_Type': device_type,

            'Location': location,

            'Is_International': is_international,

            'Previous_Transactions': previous_transactions,

            'Average_Spend': average_spend,

            'Account_Age_Days': account_age_days,

            'Suspicious_Keyword': suspicious_keyword,

            'Month': month,

            'Weekday': weekday,

            'Is_Weekend': is_weekend,

            'Spend_Deviation': spend_deviation,

            'Spend_Ratio': spend_ratio,

            'High_Value_Transaction': high_value_transaction,

            'Customer_Activity_Score': customer_activity_score,

            'Transactions_Per_Day': transactions_per_day
        }

        # =====================================
        # CONVERT TO DATAFRAME
        # =====================================

        input_df = pd.DataFrame([input_data])

        # Match feature order
        input_df = input_df[feature_names]

        # =====================================
        # PREDICTION
        # =====================================

        prediction = model.predict(input_df)[0]

        probability = model.predict_proba(
            input_df
        )[0][1]

        # =====================================
        # OUTPUT
        # =====================================

        st.subheader("Prediction Result")

        if prediction == 1:

            st.error(
                "⚠ Fraudulent Transaction Detected"
            )

        else:

            st.success(
                "✓ Genuine Transaction"
            )

        st.write(
            f"Fraud Probability: {probability:.2f}"
        )

        # =====================================
        # RISK LEVEL
        # =====================================

        if probability >= 0.8:

            st.error("Risk Level: HIGH")

        elif probability >= 0.5:

            st.warning("Risk Level: MEDIUM")

        else:

            st.success("Risk Level: LOW")

    st.markdown("""
    <div class="footer">
        Developed by 
        <span class="highlight">Vaibhav</span>
        • Powered by Streamlit 🚀
    </div>
    """, unsafe_allow_html=True)