import requests
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from base64 import b64encode, b64decode

from config import SWARM_NODE_URL, KEY_PAIR_PATH

def new_claim(uuid, msg):
    payload = {'extension':'tangleid', 'command':'new_claim', 'uuid':str(uuid), 'msg':str(msg)}
    r = requests.post(SWARM_NODE_URL, json=payload)

    return r.text

def get_claim_info(hash_txn):
    payload = {'extension':'tangleid', 'command':'get_claim_info', 'hash_txn':str(hash_txn)}
    r = requests.post(tangleid_url, json=payload)

    return r.text

def add_txn_hash(txn_hash, prize_result):
    prize_result["transation"] = txn_hash

    return prize_result

def sig_claim(txn_hash, prize_result):
    # Get private key
    file_pri_key = open(KEY_PAIR_PATH + "pri.key")
    private_key = file_pri_key.read()
    rsakey = RSA.importKey(private_key)
    file_pri_key.close()

    # Base64 deconde
    data = b64encode(txn_hash.encode())

    # Sig the claim
    signer = PKCS1_v1_5.new(rsakey)
    digest = SHA256.new()
    digest.update(b64decode(data))
    signature = signer.sign(digest)

    prize_result["credentials"]["signature"]["signatureValue"] = b64encode(signature).decode('UTF-8')

    return prize_result
