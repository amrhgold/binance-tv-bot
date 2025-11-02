from flask import Flask, request
from binance.client import Client
import os, json

app = Flask(__name__)

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

client = Client(API_KEY, API_SECRET)

@app.route('/')
def home():
    return "🚀 Binance Trading Bot is running!"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json(force=True)
    print("Webhook data:", data)

    try:
        if data.get('signal') == 'buy':
            symbol = data.get('symbol', 'BTCUSDT')
            qty = float(data.get('quantity', 0.001))
            order = client.order_market_buy(symbol=symbol, quantity=qty)
            return {'code': 'success', 'message': f'Buy order executed for {symbol}'}
        else:
            return {'code': 'ignored', 'message': 'No valid signal'}
    except Exception as e:
        print("Error:", e)
        return {'code': 'error', 'message': str(e)}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)))
