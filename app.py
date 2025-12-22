from flask import Flask, jsonify
import requests, time

app = Flask(__name__, static_url_path='', static_folder='static')

rate_cache = {"ts": 0, "rates": {}}
TTL = 3600

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/api/rate/<currency>')
def rate(currency):
    now = time.time()
    if now - rate_cache["ts"] > TTL or currency not in rate_cache["rates"]:
        try:
            r = requests.get(f"https://open.er-api.com/v6/latest/{currency}")
            if r.status_code == 200:
                data = r.json()
                rate_cache["rates"][currency] = data["rates"]
                rate_cache["ts"] = now
        except:
            pass
    cny_rate = rate_cache.get("rates", {}).get(currency, {}).get("CNY", 1)
    return jsonify({"status": "success", "rate": cny_rate})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
