from flask import Flask, request, jsonify
import datetime
import requests
import os

app = Flask(__name__)

GOOGLE_SHEET_WEBHOOK = os.environ.get("GOOGLE_SHEET_WEBHOOK")

@app.route('/log', methods=['POST'])
def log():
    data = request.json
    insight = data.get("insight", "")
    special_day = data.get("special_day", "")

    if not insight:
        return jsonify({"error": "Missing insight text"}), 400

    now = datetime.datetime.now(datetime.timezone.utc).astimezone()
    date = now.strftime("%Y-%m-%d")
    time = now.strftime("%I:%M %p")
    day = now.strftime("%A")

    payload = {
        "insight": insight,
        "tags": [],  # Tags disabled for now
        "specialDay": special_day
    }

    response = requests.post(GOOGLE_SHEET_WEBHOOK, json=payload)
    if response.ok:
        return jsonify({"message": "Logged successfully", "tags": []})
    else:
        return jsonify({"error": "Failed to log to sheet", "details": response.text}), 500

@app.route('/')
def home():
    return "Insight Logger is running"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
