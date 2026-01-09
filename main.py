from flask import Flask, request
from kiteconnect import KiteConnect
import os

app = Flask(__name__)

# Zerodha API Credentials (Set these in Render/Railway Environment Variables)
api_key = os.getenv("KITE_API_KEY")
access_token = os.getenv("KITE_ACCESS_TOKEN") 
kite = KiteConnect(api_key=api_key)
kite.set_access_token(access_token)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    # Logic to place order
    try:
        order_id = kite.place_order(
            variety=kite.VARIETY_REGULAR,
            exchange=kite.EXCHANGE_NSE,
            tradingsymbol=data['ticker'],
            transaction_type=kite.TRANSACTION_TYPE_BUY if data['action'] == 'buy' else kite.TRANSACTION_TYPE_SELL,
            quantity=data['quantity'],
            product=kite.PRODUCT_MIS,
            order_type=kite.ORDER_TYPE_MARKET
        )
        return {"status": "success", "order_id": order_id}, 200
    except Exception as e:
        return {"status": "error", "message": str(e)}, 400

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.getenv("PORT", 5000))