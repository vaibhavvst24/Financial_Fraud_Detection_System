import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def show_eda():
    st.markdown("""
    <style>

    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}

    /* Remove top padding */
    .block-container {
        padding-top: 1rem;
    }

    </style>
    """, unsafe_allow_html=True)

    # =========================================================
    # CUSTOM STYLES
    # =========================================================
    st.markdown("""
    <style>
    .stApp {
        background: #1c1c1c;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        padding: 20px;
    }
    .main_title {
        font-size: 34px;
        font-weight: bold;
        color: #f8f4f0; !important;
        margin-top: 7;
        margin-bottom: 7px;
        text-align: center;
    }
    /* ==============================
    MAIN TITLE (H1)
    ============================== */

    h1 {
        text-align: center;
        font-size: 40px !important;
        font-weight: 680 !important;
        color: #FAFA33 !important;
        margin-top: 30px !important;
        letter-spacing: 1px;
    }

    /* ==============================
    SECTION HEADINGS (H2)
    ============================== */

    h2 {
        text-align: center;
        font-size: 32px !important;
        font-weight: 600 !important;
        color: #FAFA33 !important;
        margin-top: 25px !important;
        margin-bottom: 15px !important;
        padding: 8px;
        border-radius: 10px;
        background: #3C4142;
        transition: all 0.3s ease;
        border-color: black;
    }

    /* ==============================
    SUB SECTION HEADINGS (H3)
    ============================== */

    h3 {
        text-align: center;
        font-size: 24px !important;
        font-weight: 600 !important;
        color: #FAFA33 !important;
        padding: 8px;
        border-radius: 10px;
        background: #3C4142;
        margin-top: 20px !important;
        margin-bottom: 15px !important;
        transition: all 0.3s ease;
    }

    /* ==============================
    OPTIONAL HOVER EFFECT
    ============================== */

    h1:hover,
    h2:hover,
    h3:hover {
        transform: translateY(-2px);
        transition: all 0.4s ease;
        background: #0F172B;
        color: #FAFA33 !important;
        border-color: #FAFA33;
    }

    .insight-card {
        background-color: #1c1f26;
        padding: 20px;
        border-radius: 12px;
        border-left: 5px solid #FFDF20;
        margin-bottom: 10px;
    }
    .insight-card:hover {
        transform: translateY(-4px);
        background: rgba(255,255,255,0.1);
        box-shadow: 0px 8px 20px rgba(0,0,0,0.5);
    }

    [data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid rgba(0,0,0,1);
        padding: 5px;
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

    # =========================================================
    # LOAD DATA
    # =========================================================

    @st.cache_data

    def load_data():
        df = pd.read_csv("data/Fraud_raw.csv")

        df['Transaction_Date'] = pd.to_datetime(df['Transaction_Date'], format='%d-%m-%Y %H:%M', errors='coerce')

        # Extract time features
        df['Hour'] = df['Transaction_Date'].dt.hour
        df['Day'] = df['Transaction_Date'].dt.day_name()
        df['Month'] = df['Transaction_Date'].dt.month_name()

        # Late Night Flag
        df['Late_Night_Transaction'] = df['Hour'].apply(
            lambda x: 1 if x >= 0 and x <= 5 else 0
        )

        # Spend Difference
        df['Spend_Deviation'] = (
            df['Transaction_Amount'] - df['Average_Spend']
        )

        return df


    df = load_data()

    # =========================================================
    # SIDEBAR
    # =========================================================

    st.sidebar.title("🔍 Dashboard Filters")

    merchant_filter = st.sidebar.multiselect(
        "Merchant Category",
        options=df['Merchant_Category'].unique(),
        default=df['Merchant_Category'].unique()
    )

    payment_filter = st.sidebar.multiselect(
        "Payment Method",
        options=df['Payment_Method'].unique(),
        default=df['Payment_Method'].unique()
    )

    location_filter = st.sidebar.multiselect(
        "Location",
        options=df['Location'].unique(),
        default=df['Location'].unique()
    )

    filtered_df = df[
        (df['Merchant_Category'].isin(merchant_filter)) &
        (df['Payment_Method'].isin(payment_filter)) &
        (df['Location'].isin(location_filter))
    ]

    # =========================================================
    # TITLE
    # =========================================================

    st.markdown("""<h1> 🚨 Real-Time Financial Fraud Detection System </h1>""",unsafe_allow_html=True)
    st.markdown("---")

    # =========================================================
    # KPI SECTION
    # =========================================================

    fraud_count = filtered_df['Fraudulent'].sum()

    total_transactions = len(filtered_df)

    fraud_rate = (fraud_count / total_transactions) * 100

    avg_amount = filtered_df['Transaction_Amount'].mean()

    international_fraud = filtered_df[
        (filtered_df['Is_International'] == 1) &
        (filtered_df['Fraudulent'] == 1)
    ].shape[0]

    col1, col2, col3, col4, col5, col6= st.columns(6)

    with col1:
        st.metric("💰 Total Transactions", f"{total_transactions:,}")

    with col2:
        st.metric("🚨 Fraud Transactions", f"{fraud_count:,}")

    with col3:
        st.metric("🚀 Fraud Rate", f"{fraud_rate:.2f}%")

    with col4:
        st.metric("💸 Avg Transaction", f"₹ {avg_amount:,.0f}")
    with col5:
        risky_payment = (
            df.groupby('Payment_Method')['Fraudulent'].mean().sort_values(ascending=False).index[0])

        st.metric(
            "💳 Riskiest Payment Method",
            risky_payment
        )
    with col6:
        high_risk = df[
            df['Transaction_Amount'] > (df['Average_Spend'] * 2)
        ].shape[0]

        st.metric(
            "💀 High-Risk Transactions",
            f"{high_risk:,}"
        )
        
    # =========================================================
    # FRAUD DISTRIBUTION
    # =========================================================
    st.markdown("""<h2> 🚨 Fraud Insights</h2>""", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:

        fraud_dist = filtered_df['Fraudulent'].value_counts().reset_index()
        fraud_dist.columns = ['Fraudulent', 'Count']

        fig = px.pie(
            fraud_dist,
            names='Fraudulent',
            values='Count',
            color_discrete_sequence=['#C2B280', '#FFDF20'],
            title='Fraud vs Non-Fraud Transactions',
            hole=0.5
        )

        fig.update_traces(textposition='inside', textinfo='percent',marker_line=dict(color='#000047', width=1), marker=dict(line=dict(color='#000047', width=1)), textfont_color='black')
        fig.update_layout(title={
            'text': "Fraud vs Non-Fraud Transactions",
            'x': 0.46,
            'xanchor': 'center'
            }
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:

        fraud_by_payment = filtered_df.groupby('Payment_Method')['Fraudulent'].mean().reset_index()

        fraud_by_payment['Fraudulent'] *= 100

        fig = px.bar(
            fraud_by_payment,
            x='Payment_Method',
            y='Fraudulent',
            color='Fraudulent',
            color_continuous_scale='cividis',
            title='Fraud Rate by Payment Method',
            text_auto='.2f'
        )

        fig.update_traces(texttemplate='%{y:.2f}%', textposition='outside')
        fig.update_layout(title={
            'text': "Fraud Rate by Payment Method",
            'x': 0.46,
            'xanchor': 'center'
            }
        )
        st.plotly_chart(fig, use_container_width=True)

    # =========================================================
    # INTERNATIONAL TRANSACTIONS ANALYSIS
    # =========================================================

    st.markdown("""<h2> 🌍 International Transaction Fraud Analysis</h2>""", unsafe_allow_html=True)

    intl_analysis = filtered_df.groupby('Is_International')['Fraudulent'].mean().reset_index()
    intl_analysis['Fraudulent'] *= 100
    intl_analysis['Is_International'] = intl_analysis['Is_International'].map(
        {
            0: 'Domestic',
            1: 'International'
        }
    )

    fig = px.bar(
        intl_analysis,
        x='Is_International',
        y='Fraudulent',
        color='Fraudulent',
        color_continuous_scale='cividis',
        text_auto='.2f',
        title='International Transactions Have Higher Fraud Rates'
    )

    fig.update_traces(texttemplate='%{y:.2f}%', textposition='outside')
    fig.update_layout(title={
        'text': "International Transactions Have Higher Fraud Rates",
        'x': 0.47,
        'xanchor': 'center'
    })
    st.plotly_chart(fig, use_container_width=True)

    # =========================================================
    # MERCHANT CATEGORY ANALYSIS
    # =========================================================

    col1, col2 = st.columns(2)

    with col1:

        merchant_fraud = filtered_df.groupby('Merchant_Category')['Fraudulent'].sum().reset_index()

        merchant_fraud = merchant_fraud.sort_values(
            by='Fraudulent',
            ascending=False
        )

        fig = px.bar(
            merchant_fraud,
            x='Merchant_Category',
            y='Fraudulent',
            color='Fraudulent',
            color_continuous_scale='cividis',
            title='Fraud Concentration by Merchant Category'
        )

        fig.update_traces(texttemplate='%{y}', textposition='outside')
        fig.update_layout(title={
            'text': "Fraud Concentration by Merchant Category",
            'x': 0.46,
            'xanchor': 'center'
            }
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:

        device_analysis = filtered_df.groupby('Device_Type')['Fraudulent'].mean().reset_index()

        device_analysis['Fraudulent'] *= 100

        fig = px.bar(
            device_analysis,
            x='Device_Type',
            y='Fraudulent',
            color='Fraudulent',
            color_continuous_scale='cividis',
            title='Fraud Probability by Device Type',
            text_auto='.2f'
        )
        
        fig.update_traces(texttemplate='%{y:.2f}%', textposition='outside')
        fig.update_layout(title={
            'text': "Fraud Probability by Device Type",
            'x': 0.46,
            'xanchor': 'center'
            }
        )
        st.plotly_chart(fig, use_container_width=True)

    # =========================================================
    # LATE NIGHT FRAUD ANALYSIS
    # =========================================================

    st.markdown("""<h2> 🌙 Late Night Fraud Analysis</h2>""", unsafe_allow_html=True)

    hourly_fraud = filtered_df.groupby('Hour')['Fraudulent'].mean().reset_index()

    hourly_fraud['Fraudulent'] *= 100

    fig = px.line(
        hourly_fraud,
        x='Hour',
        y='Fraudulent',
        markers=True,
        title='Fraud Rate Across Hours of the Day'
    )

    fig.add_vrect(
        x0=0,
        x1=5,
        fillcolor='red',
        opacity=0.2,
        annotation_text='Late Night Risk Zone',
        line_width=0
    )

    fig.update_layout(title={
        'text': "Fraud Rate Across Hours of the Day",
        'x': 0.48,
        'xanchor': 'center'
    })
    st.plotly_chart(fig, use_container_width=True)

    # =========================================================
    # TRANSACTION AMOUNT VS AVERAGE SPEND
    # =========================================================

    st.markdown("""<h2> 💰 Fraudulent Amount vs Customer Average Spend</h2>""", unsafe_allow_html=True)

    sample_df = filtered_df.sample(min(1000, len(filtered_df)))
    sample_df['Fraud_Label'] = sample_df['Fraudulent'].map({
        0: 'Safe',
        1: 'Fraud'
    })

    fig = px.scatter(
        sample_df,
        x='Average_Spend',
        y='Transaction_Amount',
        color='Fraud_Label',
        color_discrete_map={
            'Safe': '#31C950',
            'Fraud': '#E7180B'
        },
        title='Fraudulent Transactions Exceed Average Customer Spending',
        opacity=0.9
    )

    fig.update_traces(marker_size=8,line=dict(width=0.8, color='white'))
    fig.update_layout(title={
        'text': "Fraudulent Transactions Exceed Average Customer Spending",
        'x': 0.47,
        'xanchor': 'center'
    })
    st.plotly_chart(fig, use_container_width=True)

    # =========================================================
    # ACCOUNT AGE ANALYSIS
    # =========================================================

    col1, col2 = st.columns(2)

    with col1:

        fig = px.box(
            filtered_df,
            x='Fraudulent',
            y='Account_Age_Days',
            color='Fraudulent',
            color_discrete_map={
                0: '#2E2EFF',
                1: '#FFDF20'
            },
            title='New Accounts Show More Suspicious Behavior'
        )

        fig.update_layout(title={
            'text': "New Accounts Show More Suspicious Behavior",
            'x': 0.46,
            'xanchor': 'center'
            }
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:

        suspicious_keyword = filtered_df.groupby('Suspicious_Keyword')['Fraudulent'].sum().reset_index()

        suspicious_keyword = suspicious_keyword.sort_values(
            by='Fraudulent',
            ascending=False
        )

        fig = px.bar(
            suspicious_keyword,
            x='Suspicious_Keyword',
            y='Fraudulent',
            color='Fraudulent',
            color_continuous_scale='cividis',
            title='Top Suspicious Keywords in Fraud Cases'
        )

        fig.update_traces(texttemplate='%{y}', textposition='outside')
        fig.update_layout(title={
            'text': "Top Suspicious Keywords in Fraud Cases",
            'x': 0.46,
            'xanchor': 'center'
            }
        )
        st.plotly_chart(fig, use_container_width=True)

    # =========================================================
    # CORRELATION HEATMAP
    # =========================================================

    st.markdown("""<h3> 📊 Correlation Heatmap </h3>""", unsafe_allow_html=True)
    numeric_df = filtered_df.select_dtypes(include=np.number)

    corr = numeric_df.corr()

    fig = px.imshow(
        corr,
        text_auto=True,
        aspect='auto',
        color_continuous_scale='cividis'
    )

    fig.update_traces(texttemplate='%{z:.2f}', textfont_size=10,  textfont_color='black', selector=dict(type='heatmap'), xgap=1, ygap=1
    )
    fig.update_layout(plot_bgcolor='black')
    st.plotly_chart(fig, use_container_width=True)

    # =========================================================
    # FRAUD TREND OVER TIME
    # =========================================================

    st.markdown("""<h3> 📈 Fraud Trend Over Time </h3>""", unsafe_allow_html=True)
    trend_df = filtered_df.groupby(filtered_df['Transaction_Date'].dt.date)['Fraudulent'].sum().reset_index()
    trend_df.columns = ['Date', 'Fraud_Count']

    fig = px.area(
        trend_df,
        x='Date',
        y='Fraud_Count',
        color_discrete_sequence=['#4169e1'],
    )

    st.plotly_chart(fig, use_container_width=True)

    # =========================================================
    # Fraud Heatmap by Hour vs Payment Method
    # =========================================================

    st.markdown("""<h3> Fraud Heatmap by Hour vs Payment Method </h3>""", unsafe_allow_html=True)
    heatmap_data = df.pivot_table(
        values='Fraudulent',
        index='Payment_Method',
        columns='Hour',
        aggfunc='mean'
    )

    fig = px.imshow(
        heatmap_data,
        aspect='auto',
        color_continuous_scale='cividis'
    )

    fig.update_traces(texttemplate='%{z:.2f}', textfont_size=12, selector=dict(type='heatmap'), zmin=0, zmax=1, xgap=1, ygap=1, textfont_color='black')
    fig.update_layout(plot_bgcolor='black')
    st.plotly_chart(fig, use_container_width=True)

    # =================================================================
    # Fraud Heatmap by Hour vs Payment Method AND Fraud by Day of Week
    # =================================================================

    col1, col2 = st.columns(2)
    with col1:
        fig = px.box(
        df,
        x='Fraudulent',
        y='Transaction_Amount',
        color='Fraudulent',
        color_discrete_map={
            0: '#C4B454',
            1: '#FFDF20'
        },
        title='Transaction Amount Distribution'
        )
        
        fig.update_layout(title={
            'text': "Transaction Amount Distribution",
            'x': 0.46,
            'xanchor': 'center'
        })
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fraud_day = df.groupby('Day')['Fraudulent'].mean().reset_index()

        fraud_day['Fraudulent'] *= 100

        fig = px.bar(
            fraud_day,
            x='Day',
            y='Fraudulent',
            color='Fraudulent',
            color_continuous_scale='cividis',
            title='Fraud Rate by Day of Week'
        )

        fig.update_traces(texttemplate='%{y:.2f}%', textposition='outside')
        fig.update_layout(title={
            'text': "Fraud Rate by Day of Week",
            'x': 0.46,
            'xanchor': 'center'
        })
        st.plotly_chart(fig, use_container_width=True)

    # =================================================================
    # Fraud Rate by Location 
    # =================================================================

    st.markdown("""<h3> Fraud Rate by Location </h3>""", unsafe_allow_html=True)
    location_fraud = df.groupby('Location')['Fraudulent'].sum().reset_index()
    fig = px.bar(
        location_fraud,
        x='Location',
        y='Fraudulent',
        color='Fraudulent',
        color_continuous_scale='cividis',
    )

    fig.update_traces(texttemplate='%{y:.2f}%', textposition='outside')
    st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)
    # =================================================================
    # FRAUD RISK GAUGE AND FRAUD TRANSACTION DENSITY
    # =================================================================

    with col1:
        fraud_rate = (df['Fraudulent'].mean()) * 100

        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = fraud_rate,
            title = {'text': "Current Fraud Risk"},
            gauge = {
                'axis': {'range': [0, 100]},
                'bar': {'color': "#ff4b4b"},
                'steps': [
                    {'range': [0, 30], 'color': "green"},
                    {'range': [30, 70], 'color': "orange"},
                    {'range': [70, 100], 'color': "red"}
                ]
            }
        ))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.violin(
            df,
            x='Fraudulent',
            y='Transaction_Amount',
            color='Fraudulent',
            box=True,
            title='Fraud Transaction Density'
        )

        fig.update_layout(title={
            'text': "Fraud Transaction Density",
            'x': 0.46,
            'xanchor': 'center'
        })
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("""<h3> Multivariate Analysis: Key Features vs Fraud </h3>""", unsafe_allow_html=True)
    fig = px.scatter_matrix(
        df,
        dimensions=[
            'Transaction_Amount',
            'Average_Spend',
            'Previous_Transactions',
            'Account_Age_Days'
        ],
        color='Fraudulent',
        color_discrete_sequence={
            0: '#00cc96',
            1: '#ff4b4b'
        }
    )

    fig.update_layout(height=800, width=800)
    st.plotly_chart(fig, use_container_width=True)
    # =========================================================
    # RAW DATA
    # =========================================================

    st.markdown("""<h3> 🧾 Transaction Dataset </h3>""", unsafe_allow_html=True)
    st.dataframe(filtered_df)

    # Total Products
    st.markdown("<h3> Top 10 High-Risk Transactions</h3>", unsafe_allow_html=True)
    tfd = df[df['Fraudulent'] == 1].sort_values(
        by='Transaction_Amount',
        ascending=False
    ).head(10)

    tf = pd.DataFrame(tfd)
    st.dataframe(tf)

    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("<h3> Payment Method Most Used in Fraud</h3>", unsafe_allow_html=True)
        pm = df[df['Fraudulent'] == 1][
            'Merchant_Category'
        ].value_counts()

        pmf = pd.DataFrame(pm)
        st.dataframe(pmf)

    with col2:
        st.markdown("<h3> Fraud Ratio by Merchant Category</h3>", unsafe_allow_html=True)
        merchant_fraud = df.groupby(
            'Merchant_Category'
        )['Fraudulent'].mean() * 100

        fr = merchant_fraud.sort_values(
            ascending=False
        )

        fmc = pd.DataFrame(fr)
        st.dataframe(fmc)

    with col3:
        st.markdown("<h3> Highest Fraud amount customers</h3>", unsafe_allow_html=True)
        CH = df[df['Fraudulent'] == 1].groupby(
            'Customer_ID'
        )['Transaction_Amount'].sum().sort_values(
            ascending=False
        ).head(8)

        CHA = pd.DataFrame(CH)
        print("Suspicious Customer")
        st.dataframe(CHA)

    # Insights
    st.markdown("<hr style='border:1px solid #333'>", unsafe_allow_html=True)
    st.header("💡 Key Data Insights")
    insights = [
        "<b>International transactions</b> have higher fraud rates compared to domestic transactions",
        "Certain payment methods are more vulnerable to fraud, with some showing significantly <b>higher fraud rates</b>",
        "Fraud is concentrated in specific merchant categories, indicating that certain industries are more targeted by <b>fraudsters</b>",
        "Fraud transactions occur more during <b>late-night hours</b>, suggesting that fraudsters may prefer to operate when monitoring is lower",
        "Fraudulent amounts significantly exceed average customer spending, indicating that fraudsters often attempt to make large transactions to maximize gains",
        "<b>New accounts</b> show suspicious behavior, with a higher likelihood of being involved in fraud compared to older accounts",
        "<b>Device type</b> influences fraud probability, with certain devices being more commonly associated with fraudulent transactions"
    ]
    for ins in insights:
        st.markdown(f"<div class='insight-card'>{ins}</div>", unsafe_allow_html=True)
    # =========================================================
    # FOOTER
    # =========================================================

    st.markdown("---")
    st.markdown("""
    <div class="footer">
        Developed by 
        <span class="highlight">Vaibhav</span>
        • Powered by Streamlit 🚀
    </div>
    """, unsafe_allow_html=True)
