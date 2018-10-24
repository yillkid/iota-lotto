import json
import random
import requests
import time

from dlt import get_all_prizes 

from config import ALL_PRIZE_PATH, CLAIM_TEMPLATE_PATH

def get_all_prize():
    content_all_prize = []

    file_all_prize = open(ALL_PRIZE_PATH, "r")
    content_all_prize = file_all_prize.read()
    file_all_prize.close()

    try:
        return json.loads(content_all_prize)
    except:
        print("Error: Cannot get prize data.")
        return []

def check_duplicate_prize():
    list_all_prize = get_all_prize()
    if len(list_all_prize) is 0:
        return

    for index in range(len(list_all_prize)):
        list_txn = get_all_prizes(list_all_prize[index]["id"])
        if len(list_txn) is not 0:
            return False

    return True

def check_prize_quota(prize_result):
    list_all_prize = get_all_prize()
    if len(list_all_prize) <= int(prize_result["counts"]):
        return True
    else:
        return True

def format_prize_to_did(prize):
    file_claim_did = open(CLAIM_TEMPLATE_PATH + "prize.json", "r")
    prize_result = json.loads(file_claim_did.read())
    file_claim_did.close()

    datetime_now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.localtime())

    # Prize content
    prize_result["credentials"]["claim"]["lottery"]["prize"] = prize["describe"]
    prize_result["credentials"]["claim"]["lottery"]["time"] = datetime_now

    return prize_result

def win_prize():
    list_all_prize = get_all_prize()
    if len(list_all_prize) is 0:
        return

    # FIXME: Add lost probability
    prize_result = list_all_prize[random.randint(0,len(list_all_prize)-1)]

    # Check prize quota
    # FIXME: format lost prize to DID
    if not check_prize_quota(prize_result):
        return "lost prize"

    else:
        return format_prize_to_did(prize_result)
