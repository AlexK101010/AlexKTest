# app.py – Web-Dashboard mit Streamlit
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Daten laden
logfile = "bot_log.csv"
df = pd.read_csv(logfile)
df['timestamp'] = pd.to_datetime(df['timestamp'])

st.set_page_config(page_title="KI Trading Bot Dashboard", layout="wide")
st.title("🤖 KI Trading Bot Dashboard")

# Filteroptionen
symbols = st.multiselect("Wähle Coins aus:", df['symbol'].unique(), default=list(df['symbol'].unique()))
filtered_df = df[df['symbol'].isin(symbols)]

# Plot 1: Aktionenzähler
st.subheader("📊 Verteilung der Trading-Aktionen")
fig1, ax1 = plt.subplots()
sns.countplot(data=filtered_df, x='action', order=['Buy', 'Sell', 'Hold'], ax=ax1)
ax1.set_ylabel("Anzahl")
ax1.set_xlabel("Aktion")
st.pyplot(fig1)

# Plot 2: Sentiment Verlauf
st.subheader("📈 Sentiment-Verlauf")
fig2, ax2 = plt.subplots(figsize=(10, 4))
for symbol in filtered_df['symbol'].unique():
    sub = filtered_df[filtered_df['symbol'] == symbol]
    ax2.plot(sub['timestamp'], sub['sentiment'], label=symbol)
ax2.set_ylabel("Sentiment")
ax2.set_xlabel("Zeit")
ax2.legend()
st.pyplot(fig2)

# Plot 3: Reward Verlauf
st.subheader("💰 Kumulierte Rewards")
fig3, ax3 = plt.subplots(figsize=(10, 4))
for symbol in filtered_df['symbol'].unique():
    sub = filtered_df[filtered_df['symbol'] == symbol]
    ax3.plot(sub['timestamp'], sub['reward'].cumsum(), label=symbol)
ax3.set_ylabel("Gesamt-Reward")
ax3.set_xlabel("Zeit")
ax3.legend()
st.pyplot(fig3)

st.info("Daten aus: bot_log.csv – automatisch generiert durch den Trading Bot")
