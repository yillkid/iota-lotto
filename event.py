import json
from config import FILE_EVENT

def format_event(status, message):
    file_claim_did = open(FILE_EVENT, "r")
    result = json.loads(file_claim_did.read())
    file_claim_did.close()

    result["status"] = status
    result["message"] = message

    return result

