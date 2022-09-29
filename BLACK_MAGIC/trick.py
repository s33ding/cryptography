from email import message
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

def encrypt():
    simple_key = get_random_bytes(32)
    salt = simple_key

    password = "mypassword"
    key = PBKDF2(password, salt, dkLen=32)
    message = b"THE BLACK BOX IS OPENED!"
    cipher = AES.new(key, AES.MODE_CBC)
    ciphered_data = cipher.encrypt(pad(message, AES.block_size))

    with open('encrypted.bin', 'wb') as f:
        f.write(cipher.iv)
        f.write(ciphered_data)

    print("YOUR SECRET IS SAFE IN THE SHADOWS!")