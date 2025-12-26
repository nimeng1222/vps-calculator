from flask import Flask, jsonify, send_from_directory
import requests
import os

app = Flask(__name__, static_folder='static')

EXCHANGE_API_URL = "https://api.exchangerate-api.com/v4/latest/CNY"
BACKUP_API_URL = "https://open.er-api.com/v6/latest/CNY"

rate_cache = {}

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/api/rate/<currency>')
def get_rate(currency):
    try:
        if currency in rate_cache:
            return jsonify({'status': 'success', 'rate': rate_cache[currency], 'source': 'cache'})
        
        try:
            response = requests.get(EXCHANGE_API_URL, timeout=5)
            data = response.json()
            if 'rates' in data and currency in data['rates']:
                rate = 1 / data['rates'][currency]
                rate_cache[currency] = rate
                return jsonify({'status': 'success', 'rate': rate, 'source': 'primary'})
        except:
            pass
        
        try:
            response = requests.get(BACKUP_API_URL, timeout=5)
            data = response.json()
            if 'rates' in data and currency in data['rates']:
                rate = 1 / data['rates'][currency]
                rate_cache[currency] = rate
                return jsonify({'status': 'success', 'rate': rate, 'source': 'backup'})
        except:
            pass
        
        default_rates = {'USD': 7.15, 'EUR': 7.85, 'GBP': 9.12, 'JPY': 0.048, 'HKD': 0.92, 'TWD': 0.23}
        if currency in default_rates:
            return jsonify({'status': 'success', 'rate': default_rates[currency], 'source': 'default'})
        
        return jsonify({'status': 'error', 'message': '无法获取汇率'}), 500
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
