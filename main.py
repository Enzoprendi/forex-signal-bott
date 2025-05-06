from flask import Flask, request
import requests

app = Flask(__name__)

BOT_TOKEN = "7990066362:AAGlUyA8MHaOnZs96BwF_I_oIYgPzgH2a1A"
CHAT_ID = "-1002464221484"

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(url, json=payload)
        print("Telegram response:", response.status_code, response.text)
    except Exception as e:
        print("Error sending Telegram message:", str(e))

@app.route("/", methods=["POST"])
def webhook():
    data = request.json
    print("Webhook received:", data)

    pair = data.get("pair", "Unknown")
    side = data.get("side", "BUY").upper()
    entry = float(data.get("entry", 0))

    # Auto-calculate 15 pip TP/SL
    pip_size = 0.01 if "JPY" not in pair else 0.1
    pip_value = pip_size * 15

    if side == "BUY":
        tp = entry + pip_value
        sl = entry - pip_value
    else:
        tp = entry - pip_value
        sl = entry + pip_value

    message = f"""
💹 *{pair}* – *{side}* Signal  
📍 *Entry*: {entry:.5f}  
🎯 *TP*: {tp:.5f}  
🛡 *SL*: {sl:.5f}  
#forex #signals #LFX
"""
    send_telegram_message(message.strip())
    return "ok"

@app.route("/", methods=["GET"])
def home():
    return "Bot is running."

port = int(os.environ.get("PORT", 3000))
app.run(host="0.0.0.0", port=port)


