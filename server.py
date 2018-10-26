from flask import Flask, Response, send_from_directory, request
from lotto import check_duplicate_prize, win_prize, \
        check_prize_quota, format_prize_to_did
from did import new_claim, add_txn_hash, get_claim_info
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


@app.route("/get_claim_content", methods = ['POST'])
def get_claim_content():
    # Get request data
    content = request.json
    
    # Claim content
    return Response(get_claim_info(content["hash"]), mimetype='application/json')

@app.route("/start", methods = ['POST'])
def start():
    # Check status
    status, message = check_status()
    if status == "finish":
        return Response(json.dumps(format_event(status, message)), mimetype='application/json')

    # Get request data
    content = request.form
    
    # Starting prize
    prize_result = win_prize(content["mid"])

    # Check prize quota
    formed_prize_result = ""
    if not check_prize_quota(prize_result):
        formed_prize_result = format_prize_to_did(content["mid"])
    else:
        formed_prize_result = format_prize_to_did(content["mid"], prize_result)

    # New claim
    txn_hash = new_claim(formed_prize_result)

    # Add txn hash
    formed_prize_result = add_txn_hash(txn_hash, formed_prize_result)

    # Response with content type
    if not check_prize_quota(prize_result, ignore = txn_hash):
        formed_prize_result = format_prize_to_did(content["mid"]) # Change to lose prize

    return Response(json.dumps(formed_prize_result), mimetype='application/json')

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
