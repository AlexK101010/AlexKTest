# KI Trading Bot 🤖📈

Ein vollautomatischer Krypto-Trading-Bot mit:
- Sentiment-Analyse via FinBERT
- Reinforcement Learning (PPO)
- E-Mail Alerts
- 24/7 Paper Trading Loop (Render oder VPS geeignet)

## 🔧 Start

```bash
pip install -r requirements.txt
python main.py
```

## ⚙️ .env Datei

Erstelle eine `.env` Datei mit folgendem Inhalt:

```
NEWSAPI_KEY=dein_newsapi_key
EMAIL_RECEIVER=deine_mail
EMAIL_SENDER=deine_bot_mail
SMTP_SERVER=smtp.mail.de
SMTP_PORT=587
SMTP_PASSWORD=dein_passwort
```
