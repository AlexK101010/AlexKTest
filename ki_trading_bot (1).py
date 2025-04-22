
import pandas as pd
import numpy as np
import datetime
import random
import os

# Dummy-Funktion zur Simulation von Preis- und Sentimentdaten
def simulate_data():
    symbols = ['BTC', 'ETH', 'XRP']
    now = datetime.datetime.utcnow()
    data = []
    for symbol in symbols:
        price = random.uniform(100, 50000)
        sentiment = random.uniform(-1, 1)
        reward = random.uniform(-10, 10)
        action = random.choice(['Buy', 'Sell', 'Hold'])
        df = pd.DataFrame({
            'timestamp': [now],
            'symbol': [symbol],
            'price': [price],
            'sentiment': [sentiment],
            'reward': [reward],
            'action': [action],
        })
        data.append(df)
    return pd.concat(data, ignore_index=True)

# Strategie-Signale berechnen (Dummy-Logik für Demo-Zwecke)
def apply_strategies(df):
    df['fibonacci_signal'] = df['price'].apply(lambda x: 'Buy' if x % 2 == 0 else 'Sell')
    df['rsi_signal'] = df['sentiment'].apply(lambda s: 'Overbought' if s > 0.5 else 'Oversold' if s < -0.5 else 'Neutral')
    df['ma200_trend'] = df['price'].apply(lambda p: 'Above MA200' if p > 10000 else 'Below MA200')
    return df

# CSV aktualisieren
def log_data(df, path="bot_log.csv"):
    if os.path.exists(path):
        old = pd.read_csv(path)
        df = pd.concat([old, df], ignore_index=True)
    df.to_csv(path, index=False)

# Bot-Ausführung
df = simulate_data()
df = apply_strategies(df)
log_data(df)

print("Log updated with strategies:", df.tail(1)[['symbol', 'fibonacci_signal', 'rsi_signal', 'ma200_trend']].to_dict(orient='records')[0])
