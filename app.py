from flask import Flask, render_template
from flask_socketio import SocketIO
import yfinance as yf
import threading
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

def fetch_stock_price(stock_symbol, interval):
    """Fetches the latest stock price in a given interval (seconds)."""
    while True:
        stock = yf.Ticker(stock_symbol)
        stock_price = stock.history(period="1d")['Close'].iloc[-1]

        socketio.emit('newprice', {'symbol': stock_symbol, 'price': stock_price})
        time.sleep(interval)

@app.route('/')
def index():
    return render_template('index.html')

# Start a background thread to fetch stock data
threading.Thread(target=fetch_stock_price, args=('AAPL', 5)).start()

if __name__ == '__main__':
    socketio.run(app, debug=True)