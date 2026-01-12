from flask import Flask, request, jsonify
from kiteconnect import KiteConnect
import os

app = Flask(__name__)

# Load from environment variables (set on Render)
API_KEY = os.environ.get('gpaco6a6f304rjvl')
ACCESS_TOKEN = os.environ.get('ioD9fUxntVfRbslF2nfjVFCNB8mtsxXt')  # Refresh daily
kite = KiteConnect(api_key=API_KEY)
kite.set_access_token(ACCESS_TOKEN)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    if not data or data.get('action') != 'BUY':
        return jsonify({'status': 'ignored'}), 200

    symbol = data.get('symbol', 'COALINDIA')
    quantity = int(data.get('quantity', 10))  # Default 10 shares
    price = float(data.get('price', 0))  # Use market order if 0

    try:
        # Place BUY order (Market order for simplicity; adjust to LIMIT if needed)
        order_id = kite.place_order(
            variety=kite.VARIETY_REGULAR,
            exchange=kite.EXCHANGE_NSE,
            tradingsymbol=symbol,
            transaction_type=kite.TRANSACTION_TYPE_BUY,
            quantity=quantity,
            product=kite.PRODUCT_CNC,  # CNC for delivery; use MIS for intraday
            order_type=kite.ORDER_TYPE_MARKET if price == 0 else kite.ORDER_TYPE_LIMIT,
            price=price if price > 0 else None,
            validity=kite.VALIDITY_DAY
        )
        return jsonify({'status': 'success', 'order_id': order_id}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)