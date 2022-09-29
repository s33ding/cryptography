from base64 import encode
from email import message
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

def encrypt_file():

    simple_key = get_random_bytes(32)
    salt = simple_key
    password = "mypassword"
    key = PBKDF2(password, salt, dkLen=32)

    with open('OUTPUT/key.bin','wb') as f:
        f.write(salt)

    with open('SOURCE/input','rb') as f:
        dark_secret =  f.read()
    
    cipher = AES.new(key, AES.MODE_CBC)
    ciphered_data = cipher.encrypt(pad(dark_secret, AES.block_size))
   
    with open('OUTPUT/encrypted.bin', 'wb') as f:
        f.write(cipher.iv)
        f.write(ciphered_data)

    print("YOUR SECRET IS SAFE IN THE SHADOWS!")

def decrypt_file():

    with open('OUTPUT/key.bin','rb') as f:
        salt = f.read()

    password = "mypassword"
    
    key = PBKDF2(password, salt, dkLen=32)
    
    with open('OUTPUT/encrypted.bin', 'rb') as f:
        iv = f.read(16)
        decrypt_data = f.read()

    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    original = unpad(cipher.decrypt(decrypt_data), AES.block_size)
    print(original.decode('utf-8'))