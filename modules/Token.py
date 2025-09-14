import json, base64, os
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
os.mkdir(DATA_DIR)
DATA_DIR = "data/token"
DATA_FILE = os.path.join(DATA_DIR, "encryption_data.json")
KEY_FILE = os.path.join(DATA_DIR, "key.json")
TOKEN_FILE = "token"  # temporäre Klartext-Datei

# -------------------------------
# Key Handling
# -------------------------------
def load_key():
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "r") as f:
            key = base64.b64decode(json.load(f)["key"])
    else:
        key = get_random_bytes(16)
        with open(KEY_FILE, "w") as f:
            json.dump({"key": base64.b64encode(key).decode()}, f)
        print("🔑 Keyfile erstellt:", KEY_FILE)
    return key

# -------------------------------
# Token verschlüsseln
# -------------------------------
def encrypt_token_file(key):
    if not os.path.exists(TOKEN_FILE):
        return  # nichts zu tun
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(TOKEN_FILE, "rb") as f:
        token = f.read()
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(token)
    data = {
        "nonce": base64.b64encode(cipher.nonce).decode(),
        "ciphertext": base64.b64encode(ciphertext).decode(),
        "tag": base64.b64encode(tag).decode()
    }
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)
    os.remove(TOKEN_FILE)
    print(f"✅ {TOKEN_FILE} verschlüsselt in {DATA_FILE} und gelöscht.")

# -------------------------------
# Token entschlüsseln
# -------------------------------
def decrypt_token(key):
    if not os.path.exists(DATA_FILE):
        raise FileNotFoundError(f"{DATA_FILE} nicht gefunden. Bitte zuerst Token verschlüsseln.")
    with open(DATA_FILE, "r") as f:
        data = json.load(f)
    nonce = base64.b64decode(data["nonce"])
    ciphertext = base64.b64decode(data["ciphertext"])
    tag = base64.b64decode(data["tag"])
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    return cipher.decrypt_and_verify(ciphertext, tag).decode()

# -------------------------------
# Hauptfunktion für Bot
# -------------------------------
def get_token():
    """
    Lädt den Key, verschlüsselt Token falls Token-Datei noch existiert,
    und gibt immer den entschlüsselten Token zurück.
    """
    key = load_key()
    if os.path.exists(TOKEN_FILE):
        encrypt_token_file(key)
    token = decrypt_token(key)
    return token
