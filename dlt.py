# coding=utf-8
from iota import Iota
from config import FULL_NODE_URL

api = Iota(FULL_NODE_URL)

def get_all_prizes(prize_id):
    dict_txn = api.find_transactions(tags = [prize_id + "C"])
    if len(dict_txn["hashes"]) > 0:
        return dict_txn["hashes"]
    else:
        return []
