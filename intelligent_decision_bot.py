
import pandas as pd
import numpy as np
import datetime
import random
import os

# Simuliere neue Daten für BTC, ETH, XRP
symbols = ['BTC', 'ETH', 'XRP']
data = []
now = datetime.datetime.utcnow()

for symbol in symbols:
    price = random.uniform(500, 30000)
    sentiment = random.uniform(-1, 1)
    reward = random.uniform(-10, 10)

    # Strategie-Signale ableiten
    fibonacci = 'Buy' if price % 2 < 1 else 'Sell'
    rsi = 'Oversold' if sentiment < -0.5 else 'Overbought' if sentiment > 0.5 else 'Neutral'
    ma200 = 'Above MA200' if price > 10000 else 'Below MA200'

    # Entscheidungsgewichtung
    if fibonacci == 'Buy' and rsi == 'Oversold' and ma200 == 'Above MA200':
        action = random.choices(['Buy', 'Hold', 'Sell'], weights=[0.7, 0.2, 0.1])[0]
    elif rsi == 'Overbought' and ma200 == 'Below MA200':
        action = random.choices(['Sell', 'Hold', 'Buy'], weights=[0.6, 0.3, 0.1])[0]
    else:
        action = random.choice(['Buy', 'Sell', 'Hold'])

    # Zeile erstellen
    data.append({
        'timestamp': now,
        'symbol': symbol,
        'price': price,
        'sentiment': sentiment,
        'reward': reward,
        'action': action,
        'fibonacci_signal': fibonacci,
        'rsi_signal': rsi,
        'ma200_trend': ma200
    })

# In DataFrame umwandeln
new_df = pd.DataFrame(data)

# In CSV speichern oder anhängen
logfile = "bot_log.csv"
if os.path.exists(logfile):
    old_df = pd.read_csv(logfile)
    df = pd.concat([old_df, new_df], ignore_index=True)
else:
    df = new_df

df.to_csv(logfile, index=False)
print("Neue Trades mit Strategieentscheidungen geloggt:", new_df[['symbol', 'action', 'fibonacci_signal', 'rsi_signal', 'ma200_trend']])
