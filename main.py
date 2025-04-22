
# main.py – Produktionsversion deines KI Trading Bots (24/7 deployfähig auf Render.com oder VPS)
# HINWEIS: API-Keys, SMTP-Passwort etc. bitte in .env-Datei auslagern (nicht hart im Code!)

import os
import ccxt
import yfinance as yf
import requests
import pandas as pd
import numpy as np
import time
from datetime import datetime, timedelta
from transformers import pipeline
from stable_baselines3 import PPO
from gym import Env
from gym.spaces import Discrete, Box
import random
import schedule
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

# 📦 .env laden
load_dotenv()
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

TRADING_SYMBOLS = ["BTC-USD", "ETH-USD", "SUI-USD", "XRP-USD", "DOGE-USD", "SOL-USD", "ADA-USD"]

sentiment_pipeline = pipeline("sentiment-analysis", model="ProsusAI/finbert")

def get_news_sentiment(query="crypto"):
    url = (
        f"https://newsapi.org/v2/everything?q={query}&from={datetime.now().strftime('%Y-%m-%d')}"
        f"&language=en&sortBy=publishedAt&apiKey={NEWSAPI_KEY}"
    )
    response = requests.get(url)
    articles = response.json().get("articles", [])
    headlines = [a["title"] for a in articles if a["title"]]
    return headlines

def analyze_sentiment(texts):
    if not texts:
        return 0.0
    sentiments = sentiment_pipeline(texts)
    scores = []
    for s in sentiments:
        if s['label'] == 'positive': scores.append(1)
        elif s['label'] == 'negative': scores.append(-1)
        else: scores.append(0)
    return np.mean(scores)

def send_email(subject, message):
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_SENDER
        msg['To'] = EMAIL_RECEIVER
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_SENDER, SMTP_PASSWORD)
        server.send_message(msg)
        server.quit()
        print("📧 E-Mail Alert gesendet.")
    except Exception as e:
        print(f"❌ Fehler beim Senden der E-Mail: {e}")

def fetch_latest_data(symbol):
    df = yf.download(tickers=symbol, period="2d", interval="1h")
    df.dropna(inplace=True)
    df["MA200"] = df["Close"].rolling(window=200, min_periods=1).mean()
    return df

class LiveTradingEnv(Env):
    def __init__(self, df, max_leverage=5):
        super().__init__()
        self.df = df.reset_index()
        self.action_space = Discrete(3 * max_leverage)
        self.observation_space = Box(low=-np.inf, high=np.inf, shape=(4,), dtype=np.float32)

    def _next_observation(self):
        row = self.df.iloc[-1]
        return np.array([
            row["Close"],
            row["MA200"],
            row["Volume"],
            random.uniform(-1, 1)
        ])

    def step(self, action):
        obs = self._next_observation()
        return obs, 0.0, True, {}

    def reset(self):
        return self._next_observation()

def run_live_simulation(symbol):
    print(f"\n🟡 Paper-Trading für {symbol}")
    df = fetch_latest_data(symbol)
    env = LiveTradingEnv(df)
    model_path = f"models/{symbol.replace('-', '_')}_ppo_model.zip"
    if not os.path.exists(model_path):
        print("❌ Kein Modell gefunden")
        return
    model = PPO.load(model_path)
    obs = env.reset()
    action, _ = model.predict(obs, deterministic=True)
    act_type = action % 3
    leverage = (action // 3) + 1
    news = get_news_sentiment(symbol.split("-")[0])
    sentiment = analyze_sentiment(news)

    signal = f"🔍 Sentiment: {sentiment:.2f}\nAktion: {['Hold','Buy','Sell'][act_type]} x{leverage}\n🗞️ News: {news[0] if news else 'keine'}"
    print(signal)
    send_email(f"[BOT ALERT] {symbol}", signal)

def scheduled_run():
    print(f"\n🕒 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    for symbol in TRADING_SYMBOLS:
        run_live_simulation(symbol)

schedule.every(1).hours.do(scheduled_run)
print("✅ Bot läuft dauerhaft (jede Stunde)")

while True:
    schedule.run_pending()
    time.sleep(10)
