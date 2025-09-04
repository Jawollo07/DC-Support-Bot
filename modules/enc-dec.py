import argparse
import base64
import json
import os
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

KEY_FILE = "key.json"
ENCRYPTION_DATA_FILE = "encryption_data.json"


# -------------------------------
# Key Handling
# -------------------------------
def generate_key():
    """Generate a new AES key."""
    return get_random_bytes(16)


def save_key(key: bytes):
    """Save key in Base64 format to key.json."""
    data = {"key": base64.b64encode(key).decode()}
    with open(KEY_FILE, "w") as f:
        json.dump(data, f)


def load_key():
    """Load AES key from key.json."""
    if not os.path.exists(KEY_FILE):
        raise FileNotFoundError("Key file not found. Generate one with --type genkey")
    with open(KEY_FILE, "r") as f:
        data = json.load(f)
    return base64.b64decode(data["key"])


# -------------------------------
# Encryption / Decryption (Bytes)
# -------------------------------
def encrypt_bytes(data: bytes, key: bytes):
    """Encrypt arbitrary bytes with AES EAX."""
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(data)
    return cipher.nonce, ciphertext, tag


def decrypt_bytes(nonce: bytes, ciphertext: bytes, tag: bytes, key: bytes):
    """Decrypt arbitrary bytes with AES EAX."""
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    return cipher.decrypt_and_verify(ciphertext, tag)


# -------------------------------
# Text Encrypt/Decrypt
# -------------------------------
def encrypt_text(text: str, key: bytes):
    return encrypt_bytes(text.encode(), key)


def decrypt_text(nonce: bytes, ciphertext: bytes, tag: bytes, key: bytes):
    return decrypt_bytes(nonce, ciphertext, tag, key).decode()


# -------------------------------
# File Encrypt/Decrypt
# -------------------------------
def encrypt_file(file_path: str, key: bytes, out_path: str):
    with open(file_path, "rb") as f:
        data = f.read()
    nonce, ciphertext, tag = encrypt_bytes(data, key)
    with open(out_path, "wb") as f:
        f.write(nonce + tag + ciphertext)  # speichern als [nonce|tag|ciphertext]


def decrypt_file(file_path: str, key: bytes, out_path: str):
    with open(file_path, "rb") as f:
        file_data = f.read()
    nonce, tag, ciphertext = file_data[:16], file_data[16:32], file_data[32:]
    plain = decrypt_bytes(nonce, ciphertext, tag, key)
    with open(out_path, "wb") as f:
        f.write(plain)


# -------------------------------
# Save/Load Encryption Data (for text mode)
# -------------------------------
def save_encryption_data(nonce, ciphertext, tag):
    data = {
        "nonce": base64.b64encode(nonce).decode(),
        "ciphertext": base64.b64encode(ciphertext).decode(),
        "tag": base64.b64encode(tag).decode()
    }
    with open(ENCRYPTION_DATA_FILE, "w") as f:
        json.dump(data, f)


def load_encryption_data():
    if not os.path.exists(ENCRYPTION_DATA_FILE):
        raise FileNotFoundError(f"{ENCRYPTION_DATA_FILE} not found. Encrypt some text first.")
    with open(ENCRYPTION_DATA_FILE, "r") as f:
        data = json.load(f)
    nonce = base64.b64decode(data["nonce"])
    ciphertext = base64.b64decode(data["ciphertext"])
    tag = base64.b64decode(data["tag"])
    return nonce, ciphertext, tag


# -------------------------------
# CLI Main
# -------------------------------
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--type", choices=["encrypt", "decrypt", "genkey"], required=True, help="Operation type")
    parser.add_argument("--mode", choices=["text", "file"], default="text", help="Encrypt/decrypt text or file")
    parser.add_argument("--text", type=str, help="Text to encrypt")
    parser.add_argument("--file", type=str, help="File path for encryption/decryption")
    parser.add_argument("--out", type=str, help="Output file for encryption/decryption (file mode)")
    args = parser.parse_args()

    # Generate Key
    if args.type == "genkey":
        key = generate_key()
        save_key(key)
        print("Generated new AES key and saved to key.json")
        return

    # Load Key
    key = load_key()
    if key is None:
        key = generate_key()
    # Encrypt
    if args.type == "encrypt":
        if args.mode == "text":
            if not args.text:
                print("❌ Please provide --text for text mode")
                return
            nonce, ciphertext, tag = encrypt_text(args.text, key)
            save_encryption_data(nonce, ciphertext, tag)
            print("✅ Text encrypted and saved to encryption_data.json")

        elif args.mode == "file":
            if not args.file:
                print("❌ Please provide --file for file mode")
                return
            out_path = args.out if args.out else args.file
            encrypt_file(args.file, key, out_path)
            print(f"✅ File encrypted → {out_path}")

    # Decrypt
    elif args.type == "decrypt":
        if args.mode == "text":
            try:
                nonce, ciphertext, tag = load_encryption_data()
                plain_text = decrypt_text(nonce, ciphertext, tag, key)
                print("✅ Decrypted text:", plain_text)
            except Exception as e:
                print("❌ Decryption failed:", str(e))

        elif args.mode == "file":
            if not args.file:
                print("❌ Please provide --file for file mode")
                return
            out_path = args.out if args.out else args.file
            try:
                decrypt_file(args.file, key, out_path)
                print(f"✅ File decrypted → {out_path}")
            except Exception as e:
                print("❌ File decryption failed:", str(e))


if __name__ == "__main__":
    main()
