from flask import Flask, send_from_directory
from lotto import check_duplicate_prize, win_prize
from did import new_claim, add_txn_hash, sig_claim
import json

from config import TXN_TAG

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route('/data/<path:path>')
def send_data(path):
    return send_from_directory('data', path)

@app.route("/prepare")
def prepare():
    # Check duplicate prize id in Tangle
    if not check_duplicate_prize():
        return "Error: Duplicate prize id in Tangle, \
                modify id field in data/prize.json file."

    return "All passed!"

@app.route("/start")
def start():
    # Starting prize
    prize_result = win_prize()

    # New claim
    txn_hash = new_claim(TXN_TAG, prize_result)

    # Add txn hash
    prize_result = add_txn_hash(txn_hash, prize_result)

    # Sig claim
    prize_result = sig_claim(txn_hash, prize_result)

    return json.dumps(prize_result)

if __name__ == "__main__":
    app.run(debug=True, threaded=True, host="0.0.0.0")
