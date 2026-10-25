"""AES-CBC encryption and PBKDF2 password hashing."""
import base64
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes


class EncryptionManager:
    def __init__(self):
        self.key = None
        self.iv = None

    def generate_key(self, size=32):
        self.key = get_random_bytes(size)
        self.iv = get_random_bytes(16)
        return self.key

    def encrypt(self, data):
        if not self.key:
            self.generate_key()
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        raw = data.encode() if isinstance(data, str) else data
        encrypted = cipher.encrypt(pad(raw, AES.block_size))
        return {
            'key': base64.b64encode(self.key).decode(),
            'iv': base64.b64encode(self.iv).decode(),
            'data': base64.b64encode(encrypted).decode(),
        }

    def decrypt(self, encrypted_dict):
        key = base64.b64decode(encrypted_dict['key'])
        iv = base64.b64decode(encrypted_dict['iv'])
        data = base64.b64decode(encrypted_dict['data'])
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(data), AES.block_size)

    def hash_password(self, password):
        salt = get_random_bytes(16)
        hashed = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
        return {
            'salt': base64.b64encode(salt).decode(),
            'hash': base64.b64encode(hashed).decode(),
        }

    def verify_password(self, password, stored_hash):
        salt = base64.b64decode(stored_hash['salt'])
        hashed = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
        return hashed == base64.b64decode(stored_hash['hash'])
