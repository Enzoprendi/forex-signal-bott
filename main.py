from flask import Flask, request
import requests

app = Flask(__name__)

# Direct values for testing (use env vars in production)
BOT_TOKEN = "7373123273:AAEWtPpbyjo8Tsy7Ym0DO-xVsbh783JXiQ8"
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
    side = data.get("side", "BUY")
    entry = data.get("entry", "N/A")
    tp = data.get("tp", "N/A")
    sl = data.get("sl", "N/A")

    message = f"""
💹 *{pair}* – *{side.upper()}* Signal  
📍 *Entry*: {entry}  
🎯 *TP*: {tp}  
🛡 *SL*: {sl}  
#forex #signals #LFX
"""
    send_telegram_message(message.strip())
    return "ok"

@app.route("/", methods=["GET"])
def home():
    return "Bot is running."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
