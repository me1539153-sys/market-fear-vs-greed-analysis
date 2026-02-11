import streamlit as st
import pandas as pd
import pickle
import os
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Trader Sentiment Dashboard", layout="wide")

st.title("📊 Trader Performance vs Market Sentiment")

# ===============================
# LOAD DATA
# ===============================

@st.cache_data
def load_data():
    trades = pd.read_csv(r"C:\Users\hp\Desktop\ml_mini_project\intern.py\historical_data.csv")
    fear_greed = pd.read_csv(r"C:\Users\hp\Desktop\ml_mini_project\intern.py\fear_greed_index.csv")
    return trades, fear_greed

trades, fear_greed = load_data()

# ===============================
# KPI SECTION
# ===============================

st.subheader("📌 Key Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("Total Trades", len(trades))
col2.metric("Average Trade Size", round(trades['Size Tokens'].mean(), 2))
col3.metric("Unique Traders", trades['Account'].nunique())

st.divider()

# ===============================
# FEAR VS GREED DISTRIBUTION
# ===============================

st.subheader("📈 Fear vs Greed Distribution")

fig1, ax1 = plt.subplots()
fear_greed['classification'].value_counts().plot(kind='bar', ax=ax1)
ax1.set_ylabel("Count")
ax1.set_xlabel("Sentiment")
st.pyplot(fig1)

# ===============================
# PROFITABILITY DISTRIBUTION
# ===============================

if 'pnl' in trades.columns:
    st.subheader("💰 Profit / Loss Distribution")

    fig2, ax2 = plt.subplots()
    sns.histplot(trades['pnl'], bins=50, kde=True, ax=ax2)
    st.pyplot(fig2)

# ===============================
# TRADES OVER TIME
# ===============================

if 'Timestamp' in trades.columns:
    trades['Timestamp'] = pd.to_datetime(trades['Timestamp'], unit='ms')
    trades['date'] = trades['Timestamp'].dt.date

    daily_trades = trades.groupby('date').size()

    st.subheader("📅 Daily Trade Volume")

    fig3, ax3 = plt.subplots()
    daily_trades.plot(ax=ax3)
    ax3.set_ylabel("Number of Trades")
    st.pyplot(fig3)

st.divider()

# ===============================
# LOAD MODEL
# ===============================

model_path = r"C:\Users\hp\Desktop\ml_mini_project\intern.py\Trader_sentiment_model.pkl"

if os.path.exists(model_path):
    with open(model_path, "rb") as file:
        model = pickle.load(file)
    st.success("Model loaded successfully!")
else:
    st.warning("Model not found. Prediction disabled.")
    model = None

# ===============================
# PREDICTION SECTION
# ===============================

if model is not None:

    st.subheader("🔮 Predict Trader Profitability")

    trades_per_day = st.number_input("Trades Per Day", min_value=0)
    avg_trade_size = st.number_input("Average Trade Size", min_value=0.0)
    long_short_ratio = st.number_input("Long / Short Ratio", min_value=0.0)
    sentiment = st.selectbox("Market Sentiment", ["Fear", "Greed", "Neutral"])

    if st.button("Predict"):

        input_data = {
            "trades_per_day": trades_per_day,
            "avg_trade_size": avg_trade_size,
            "long_short_ratio": long_short_ratio,
            "classification_Fear": 0,
            "classification_Greed": 0,
            "classification_Neutral": 0
        }

        input_data[f"classification_{sentiment}"] = 1

        input_df = pd.DataFrame([input_data])
        input_df = input_df[model.feature_names_in_]

        prediction = model.predict(input_df)[0]

        if prediction == 1:
            st.success("✅ Predicted: Profitable Day")
        else:
            st.error("❌ Predicted: Non-Profitable Day")

