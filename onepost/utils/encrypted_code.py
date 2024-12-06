from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import base64

# AES 密钥
AES_KEY = b'&8@4IWTe$rOBTDP0d$3TeiNxgcueLsAr'
cipher = AES.new(AES_KEY, AES.MODE_CBC)


def encrypt_invite_code(plaintext_code):
    padded_data = pad(plaintext_code.encode(), AES.block_size)
    encrypted_data = cipher.encrypt(padded_data)
    return base64.urlsafe_b64encode(cipher.iv + encrypted_data).decode()


def decrypt_invite_code(ciphertext_code):
    ciphertext_data = base64.urlsafe_b64decode(ciphertext_code.encode())
    iv = ciphertext_data[:AES.block_size]
    cipher_dec = AES.new(AES_KEY, AES.MODE_CBC, iv)
    decrypted_data = cipher_dec.decrypt(ciphertext_data[AES.block_size:])
    return unpad(decrypted_data, AES.block_size).decode()
