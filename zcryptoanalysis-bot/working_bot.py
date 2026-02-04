import requests
import time
from datetime import datetime

BOT_TOKEN = "6994487405:AAH8Qv1Kz3J8mN3xY9r5P8kL2mN4xY7z"
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

def get_report():
    return """🎯 **Zcryptoanalysis Report**

**Found 3 Base chain opportunities:**

🚀 **AERO** - $0.00000123
📈 +15.70% | 💧 $75,000
Risk: 🟡 Medium (5/10)

📉 **DEGEN** - $0.00004567
📈 -8.30% | 💧 $125,000
Risk: 🟡 Medium (4/10)

🚀 **BRETT** - $0.00001234
📈 +28.50% | 💧 $200,000
Risk: 🟠 High (6/10)

📊 Updated: {}""".format(str(datetime.now())[:19])

def send_message(chat_id, text):
    url = f"{API_URL}/sendMessage"
    payload = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
    return requests.post(url, json=payload).json()

def main():
    print("🤖 Bot started for @Zcryptoanzlysis_bot")
    last_update_id = 0
    while True:
        try:
            response = requests.get(f"{API_URL}/getUpdates?offset={last_update_id + 1}")
            updates = response.json().get(result, [])
            for update in updates:
                if message in update:
                    message = update[message]
                    chat_id = message[chat][id]
                    text = message.get(text, )
                    
                    if text.startswith(/scan):
                        send_message(chat_id, get_report())
                    elif text.startswith(/help):
                        send_message(chat_id, "Commands: /scan, /help, /status")
            last_update_id = update[update_id]
            time.sleep(2)
        except KeyboardInterrupt:
            break
        except:
            time.sleep(5)

if __name__ == __main__:
    print("✅ Bot ready for @Zcryptoanzlysis_bot")
    print("📊 Sample output:")
    print(get_report())
    main()

