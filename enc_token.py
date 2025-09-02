import json, base64, os
import token
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

KEY_FILE = "key.json"
DATA_FILE = "encryption_data.json"

def load_key():
    # Key laden oder erzeugen
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "r") as f:
            key = base64.b64decode(json.load(f)["key"])
    else:
        key = get_random_bytes(16)
        with open(KEY_FILE, "w") as f:
            json.dump({"key": base64.b64encode(key).decode()}, f)
        print("Keyfile erstellt:", KEY_FILE)
    return key

def token_encrypt(key):
    # Token verschlüsseln
    token = input("Discord Bot Token: ").encode()
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(token)
    data = {
        "nonce": base64.b64encode(cipher.nonce).decode(),
        "ciphertext": base64.b64encode(ciphertext).decode(),
        "tag": base64.b64encode(tag).decode()
    }
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)
    print("Token verschlüsselt in", DATA_FILE)
