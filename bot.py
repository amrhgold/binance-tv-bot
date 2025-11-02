from flask import Flask, request
from binance.client import Client
import os, json

app = Flask(__name__)

# متغيرات البيئة من Railway
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

# تأكد إنهم موجودين في الـ logs
print("🚀 Starting Flask app...")
print("API_KEY found:", bool(API_KEY))
print("API_SECRET found:", bool(API_SECRET))

client = Client(API_KEY, API_SECRET)

@app.route('/')
def home():
    return "🚀 Binance TradingView Bot is running!"

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.get_json(force=True)
        print("📩 Webhook data:", data)

        if data.get('signal') == 'buy':
            symbol = data.get('symbol', 'BTCUSDT')
            qty = float(data.get('quantity', 0.001))
            order = client.order_market_buy(symbol=symbol, quantity=qty)
            print("✅ Order executed:", order)
            return {'code': 'success', 'message': f'Buy order executed for {symbol}'}
        else:
            return {'code': 'ignored', 'message': 'No valid signal'}

    except Exception as e:
        print("❌ Error:", e)
        return {'code': 'error', 'message': str(e)}

if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    print(f"✅ Flask running on port {port}")
    app.run(host='0.0.0.0', port=port)
