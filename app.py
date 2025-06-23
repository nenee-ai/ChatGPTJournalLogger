from flask import Flask, request, jsonify
import datetime
import requests
import os

app = Flask(__name__)

# Your webhook URL from Google Apps Script must be stored as an environment variable
GOOGLE_SHEET_WEBHOOK = os.environ.get("GOOGLE_SHEET_WEBHOOK")

@app.route('/log', methods=['POST'])
def log():
    data = request.json
    insight = data.get("insight", "")
    special_day = data.get("special_day", "")

    print("Received insight:", insight)
    print("Special day:", special_day)

    if not insight:
        print("Missing insight!")
        return jsonify({"error": "Missing insight text"}), 400

    # Generate timestamp info
    now = datetime.datetime.now(datetime.timezone.utc).astimezone()
    date = now.strftime("%Y-%m-%d")
    time = now.strftime("%I:%M %p")
    day = now.strftime("%A")

    # Prepare payload
    payload = {
        "date": date,
        "time": time,
        "day": day,
        "specialDay": special_day,
        "tags": [],  # Tags disabled
        "insight": insight
    }

    print("Payload to webhook:", payload)

    # Send to Google Apps Script webhook
    try:
        response = requests.post(GOOGLE_SHEET_WEBHOOK, json=payload)
        print("Webhook response:", response.status_code, response.text)

        if response.ok:
            return jsonify({"message": "Logged successfully", "tags": []})
        else:
            return jsonify({
                "error": "Failed to log to sheet",
                "details": response.text
            }), 500
    except Exception as e:
        print("Exception during webhook POST:", str(e))
        return jsonify({
            "error": "Exception occurred while sending to webhook",
            "details": str(e)
        }), 500

@app.route('/')
def home():
    return "Insight Logger is running"

# Required for Render deployment
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
