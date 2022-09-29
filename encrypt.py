from email import message
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

simple_key = get_random_bytes(32)
print(simple_key)
salt = simple_key

password = "mypassword"

key = PBKDF2(password, salt, dkLen=32)

print(key)
message = b"Hello Secret World!"
cipher = AES.new(key, AES.MODE_CBC)
ciphered_data = cipher.encrypt(pad(message, AES.block_size))

with open('encrypted.bin', 'wb') as f:
    f.write(cipher.iv)
    f.write(ciphered_data)

print(ciphered_data)