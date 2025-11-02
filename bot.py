from flask import Flask, request
from binance.client import Client
import os
import json

app = Flask(__name__)

API_KEY = os.getenv("ZVZ1khUdE8Bb22OihiJuW92oz79uhMlfOPwaclUXRfLoWwL88aJ0d8mWjGLJijkK")
API_SECRET = os.getenv("HyVufwNGqD2rUfZaEPyv59IeTndOsFvNIKDbuP0Wl7VX4K77xcZEjf1KVqBEGwCc")

client = Client(API_KEY, API_SECRET)

@app.route('/')
def home():
    return "🚀 Binance TradingView Bot is running!"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = json.loads(request.data)

    if data.get('signal') == 'buy':
        symbol = data.get('symbol', 'BTCUSDT')
        qty = float(data.get('quantity', 0.001))
        try:
            order = client.order_market_buy(symbol=symbol, quantity=qty)
            print(order)
            return {'code': 'success', 'message': f'Buy order executed for {symbol}'}
        except Exception as e:
            return {'code': 'error', 'message': str(e)}
    else:
        return {'code': 'ignored', 'message': 'No valid signal'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)))

