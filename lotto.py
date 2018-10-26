import json
import random
import requests
import time

# from lotto import list_all_prize
from dlt import get_all_prizes_on_dlt

from config import ALL_PRIZE_PATH, CLAIM_TEMPLATE_PATH, PRIZE_STATUS

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
        list_txn = get_all_prizes_on_dlt(list_all_prize[index]["id"])
        if len(list_txn) is not 0:
            return False

    return True

def check_prize_quota(prize_result):
    list_all_dlt_prize = get_all_prizes_on_dlt(prize_result["id"])
    if len(list_all_dlt_prize) < int(prize_result["counts"]):
        return True
    else:
        return False

def format_prize_to_did(user_id, prize = ""):
    prize_template_path = CLAIM_TEMPLATE_PATH + "lose.json"

    if prize != "":
        prize_template_path = CLAIM_TEMPLATE_PATH + "prize.json"

    file_claim_did = open(prize_template_path, "r")
    prize_result = json.loads(file_claim_did.read())
    file_claim_did.close()

    datetime_now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.localtime())

    # Prize content
    prize_result["credentials"]["claim"]["mid"] = user_id
    prize_result["credentials"]["claim"]["lottery"]["time"] = datetime_now

    if prize != "":
        prize_result["credentials"]["claim"]["lottery"]["pid"] = prize["id"]
        prize_result["credentials"]["claim"]["lottery"]["prize"] = prize["describe"]

    return prize_result

def win_prize(user_id):
    # Get all prize in prize file
    list_all_prize = get_all_prize()
    if len(list_all_prize) is 0:
        return

    prize_result = list_all_prize[random.randint(0,len(list_all_prize)-1)]

    return prize_result

    # Check prize quota
#    if not check_prize_quota(prize_result):
#        return format_prize_to_did(user_id)
#    else:
#        return format_prize_to_did(user_id, prize_result)
