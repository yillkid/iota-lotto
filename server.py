from flask import Flask, Response, send_from_directory, request
from lotto import check_duplicate_prize, win_prize
from did import new_claim, add_txn_hash
from event import format_event
from config import PRIZE_STATUS
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

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

@app.route("/start", methods = ['POST'])
def start():
    # Check status
    status, message = check_status()
    if status == "finish":
        return Response(json.dumps(format_event(status, message)), mimetype='application/json')

    # Get request data
    content = request.json
    
    # Starting prize
    prize_result = win_prize(content["mid"])

    # New claim
    txn_hash = new_claim(prize_result)

    # Add txn hash
    prize_result = add_txn_hash(txn_hash, prize_result)

    # Response with content type
    return Response(json.dumps(prize_result), mimetype='application/json')

def check_status():
    status = ""
    try:
        file_status = open(PRIZE_STATUS, "r")
        status = file_status.read()
        file_status.close()
    except:
        status = "finish"

    return status, "Game Over!"

if __name__ == "__main__":
    app.run(debug=True, threaded=True, host="0.0.0.0")
