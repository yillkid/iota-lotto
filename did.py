import requests
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from base64 import b64encode, b64decode

from config import SWARM_NODE_URL, KEY_PAIR_PATH

def new_claim(msg):
    # Sign claim
    signature = sig_claim(msg["credentials"]["claim"]["mid"])
    msg["credentials"]["signature"]["signatureValue"] =  b64encode(signature).decode('UTF-8')

    # Issue claim
    payload = {'extension':'tangleid', 'command':'new_claim', 'uuid':msg["credentials"]["claim"]["lottery"]["pid"], 'msg':str(msg)}
    r = requests.post(SWARM_NODE_URL, json=payload)

    return r.text

def get_claim_info(hash_txn):
    payload = {'extension':'tangleid', 'command':'get_claim_info', 'hash_txn':str(hash_txn)}
    r = requests.post(tangleid_url, json=payload)

    return r.text

def add_txn_hash(txn_hash, prize_result):
    prize_result["transation"] = txn_hash

    return prize_result

def sig_claim(data):
    # Get private key
    file_pri_key = open(KEY_PAIR_PATH + "pri.key")
    private_key = file_pri_key.read()
    if private_key == "":
        return prize_result
    rsakey = RSA.importKey(private_key)
    file_pri_key.close()

    # Base64 deconde
    data = data.encode()

    # Sig the claim
    signer = PKCS1_v1_5.new(rsakey)
    digest = SHA256.new()
    digest.update(data)
    signature = signer.sign(digest)

    return signature

def verify(message, signature):
    # Get public key
    file_pub_key = open(KEY_PAIR_PATH + "pub.key")
    public_key = file_pub_key.read()
    if public_key == "":
        print("Error: Cannot find public key file.")
        return False
    rsakey = RSA.importKey(public_key)
    file_pub_key.close()

    # Verify
    signer = PKCS1_v1_5.new(rsakey)
    digest = SHA256.new()
    digest.update(message.encode())
    if signer.verify(digest, b64decode(signature.encode())):
        print("Success")
        return True
    else:
        print("Error: Fail")
        return False
