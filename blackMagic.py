# %%
from getpass import getpass
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA256
from cryptography.fernet import Fernet
import pandas as pd
import numpy as np
import json

# %%
def gen_key(key_file='key.bin',type_password=False, import_secret='magic'):
    simple_key = get_random_bytes(32)
    salt = simple_key
    default_password = 'magic' 
    if import_secret!=default_password:
        type_password=False
    if type_password == True:
        password = getpass()
    if type_password == False:
        password = import_secret
    key = PBKDF2(password, salt, dkLen=32)
    with open(key_file,'wb') as f:
        f.write(key)
    print("YOUR KEY WAS CREATED BY MAGIC!")


# gen_key(key_file='key.bin',type_passwd=True, import_secret='magic')
# gen_key()

# %%
def get_key(key_file='key.bin', type_password=True, import_secret='magic'):
    with open(key_file,'rb') as f:
        salt = f.read()
    
    default_password = 'magic' 
    if import_secret!=default_password:
        type_password=False
    if type_password == True:
        password = getpass()
    if type_password == False:
        password = import_secret
    key = PBKDF2(password, salt, dkLen=32)
    # print("THE KEY IS IN YOUR HANDS!")
    return key

# %%
def encrypt_file(secret_file='input_file', key_file='key.bin',output_file='encrypted.bin', import_secret='magic', type_password=False):
    with open(secret_file,'rb') as f:
        dark_secret =  f.read()
    
    key = get_key(key_file=key_file, type_password=type_password, import_secret=import_secret)
    cipher = AES.new(key, AES.MODE_CBC)
    ciphered_data = cipher.encrypt(pad(dark_secret, AES.block_size))
    with open(output_file, 'wb') as f:
        f.write(cipher.iv)
        f.write(ciphered_data)
    print("YOUR SECRET IS PROTECTED WITH ENCRYPTION!")

# %%
def decrypt_file(secret_file='encrypted.bin', key_file='key.bin',import_secret='magic',type_password=False):
    print("THE BLACK BOX IS OPENED!\n")
    key = get_key(key_file=key_file, type_password=type_password, import_secret=import_secret)
    
    with open(secret_file, 'rb') as f:
        iv = f.read(16)
        decrypt_data = f.read()

    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    original = unpad(cipher.decrypt(decrypt_data), AES.block_size)
    return original.decode('utf-8')

# decrypt_file(secret_file='encrypted.bin', key_file='key.bin',import_secret='magic',type_password=False)

# %%
def gen_fernet_key(key_file='fernet.bin'):
    key = Fernet.generate_key()
    with open(key_file,'wb') as f:
        f.write(key) 

def get_fernet_key(key_file='fernet.bin'):
    with open(key_file,'rb') as f:
        key = f.read()
    return key

def encrypt_str(text = '', key_file='fernet.bin'):
    if text==None:
        return None
    text = str(text)
    key = get_fernet_key(key_file=key_file)
    fernet = Fernet(key)
    encMessage = fernet.encrypt(text.encode())
    return encMessage.decode()

def decrypt_str( text, key_file='fernet.bin'):
    key = get_fernet_key(key_file=key_file)
    fernet = Fernet(key)
    encMessage = text.encode()
    decMessage = fernet.decrypt(encMessage).decode()
    # if decMessage.isnumeric() == True:
    #     return int(decMessage)
    return decMessage

# gen_fernet_key()


# %%
def encrypt_json_fernet(json_file='teste.json',key_file='fernet.bin'):
    with open(json_file,'r') as f:
        dct = json.load(f)
    
    for key,value in dct.items():
        dct[key] = encrypt_str(text = value, key_file=key_file)

    print(dct)
    with open('teste_output.json','w') as f:
        json.dump(dct,f,indent=4)
    

# encrypt_json_fernet()

# %%
def decrypt_json_fernet(json_file='teste.json',key_file='fernet.bin'):
    with open(json_file,'r') as f:
        dct = json.load(f)
    for key,value in dct.items():
        dct[key] = decrypt_str(text = value, key_file=key_file)
    print(dct)

# decrypt_json_fernet(json_file='teste_output.json')

# %%
df = pd.read_csv('MOCK_DATA.csv')
df['cpf_enc'] = df.cpf.apply(lambda x: encrypt_str(x))
df['cpf_dec'] = df.cpf_enc.apply(lambda x: decrypt_str(x))

# df.head()


