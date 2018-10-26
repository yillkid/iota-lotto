import json
import time

from dlt import get_all_prizes_on_dlt
from config import ALL_PRIZE_PATH, PRIZE_STATUS

def prize_dashboard():
    # Quota
    quota_flag = 1

    # Load prize file
    prize_file = open(ALL_PRIZE_PATH, "r")
    list_all_prize = json.loads(prize_file.read())
    prize_file.close()

    # Check prize result
    for index in range(len(list_all_prize)):
        list_txn = get_all_prizes_on_dlt(list_all_prize[index]["id"])
        if len(list_txn) < int(list_all_prize[index]["counts"]):
            quota_flag = 0

        print("Dashboard: prize ID: " + list_all_prize[index]["id"] + " stauts: " + str(len(list_txn)) + "/" + list_all_prize[index]["counts"])

    return quota_flag


def set_status(msg):
    file_status = open(PRIZE_STATUS, "w")
    file_status.write(msg)
    file_status.close()

set_status("process")
while True:
    time.sleep(10)
    result = prize_dashboard()
    if result == 1:
        print("Game Over!")
        set_status("finish")
        break
