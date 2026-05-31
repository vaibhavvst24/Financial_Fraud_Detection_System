# 💳 FraudShield AI – Financial Fraud Detection & Analytics Platform

## 📌 Project Overview

FraudShield AI is an end-to-end Machine Learning project designed to identify potentially fraudulent financial transactions using behavioral analytics and predictive modeling.

The platform combines Exploratory Data Analysis (EDA), Feature Engineering, Machine Learning, and an interactive Streamlit dashboard to provide real-time fraud detection and transaction risk assessment.

The objective is to help financial institutions, fintech companies, and payment systems proactively identify suspicious transactions and minimize financial losses.

---

## 🚀 Key Features

### 📊 Interactive Analytics Dashboard
Fraud vs Genuine Transaction Analysis

Transaction Amount Distribution

Payment Method Analysis

Merchant Category Insights

Device Type Fraud Trends

International vs Domestic Transaction Analysis

Fraud Risk Monitoring

Correlation Heatmap

### 🤖 Machine Learning Fraud Detection
Real-time fraud prediction

Fraud probability scoring

Risk classification (Low / Medium / High)

Behavioral anomaly detection

### 🧠 Advanced Feature Engineering

The model utilizes both raw transaction data and engineered behavioral features:

Spend Deviation
Spend Ratio
High Value Transaction Flag

---

## 🛠️ Technology Stack
### Programming Language
Python

### Data Processing
Pandas
NumPy

### Visualization
Plotly
Streamlit

### Machine Learning
Scikit-learn
Model Serialization
Pickle

### Frontend/UI
Streamlit
Custom CSS

---

# Dataset Features

| Feature                 | Description                      |
| ----------------------- | -------------------------------- |
| Transaction_Amount      | Amount involved in transaction   |
| Merchant_Category       | Merchant classification          |
| Payment_Method          | Payment mode used                |
| Device_Type             | Device used for transaction      |
| Location                | Transaction location             |
| Is_International        | Domestic or International        |
| Previous_Transactions   | Historical transaction count     |
| Average_Spend           | Customer average spending        |
| Account_Age_Days        | Age of customer account          |
| Suspicious_Keyword      | Suspicious transaction indicator |
| Month                   | Transaction month                |
| Weekday                 | Day of week                      |
| Is_Weekend              | Weekend flag                     |
| Spend_Deviation         | Difference from average spend    |
| Spend_Ratio             | Relative spending ratio          |
| High_Value_Transaction  | High amount transaction flag     |
| Customer_Activity_Score | Customer activity metric         |
| Transactions_Per_Day    | Daily transaction frequency      |

---

## ⚙️ Machine Learning Workflow
### 1️⃣ Data Preprocessing
Missing value handling
Data cleaning
Label Encoding
Feature selection

### 2️⃣ Feature Engineering

Behavioral features were created to improve fraud detection performance:
Spend_Deviation = Transaction_Amount - Average_Spend

Spend_Ratio = Transaction_Amount / Average_Spend

Transactions_Per_Day = Previous_Transactions / Account_Age_Days

Customer_Activity_Score = Previous_Transactions + Average_Spend

### 3️⃣ Model Training

The model was trained using supervised machine learning techniques to classify transactions as:
0 → Genuine Transaction
1 → Fraudulent Transaction

### 4️⃣ Prediction

The deployed model predicts:

Transaction Status
Fraud Probability
Risk Level

---

## 📈 Risk Classification
| Probability | Risk Level  |
| ----------- | ----------- |
| < 0.50      | Low Risk    |
| 0.50 – 0.79 | Medium Risk |
| ≥ 0.80      | High Risk   |

---

## 🚨 High-Risk Fraud Indicators

The system identifies suspicious activities such as:

High-value transactions

Unusual spending behavior

International transactions

High transaction frequency

Significant spend deviation

Risky payment patterns

---

## 📷 Dashboard Preview
EDA Dashboard

Fraud Analytics

Interactive Charts

Business Insights

Risk Monitoring

## Prediction Dashboard
Transaction Input Form

Real-Time Fraud Detection

Fraud Probability Score

Risk Level Classification

---

## Clone Repository
git clone https://github.com/vaibhavvst24/Financial_Fraud_Detection_System

cd FraudShield-AI

## Create Virtual Environment
python -m venv venv

## Windows
venv\Scripts\activate

## Install Dependencies
pip install -r requirements.txt

## Run Streamlit App
streamlit run main.py

---

## 📌 Future Enhancements
XGBoost & LightGBM Integration

Real-Time Transaction Streaming

SHAP Explainability Dashboard

Cloud Deployment

REST API Integration

Fraud Alert System

Geo-Location Fraud Tracking

User Authentication

---

## 📊 Business Impact

This solution helps organizations:

Detect fraudulent transactions faster

Reduce financial losses

Improve customer trust

Enhance risk management

Support fraud investigation teams

---

# 👨‍💻 Author

## Vaibhav Singh

⭐ If you found this project useful, consider giving it a star on GitHub!
