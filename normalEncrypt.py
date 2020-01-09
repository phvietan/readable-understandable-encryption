import os
import random
from Crypto import Random
from Crypto.Cipher import AES

blocksize = 32

def pad(s):
    return s + (blocksize - len(s) % blocksize) * chr(blocksize - len(s) % blocksize)

def unpad(s):
    return s[:-ord(s[len(s)-1:])]

key = os.urandom(16)
iv = os.urandom(16)

aes = AES.new(key, AES.MODE_CBC, iv)

plaintext = 'hello world'
ciphertext = iv + aes.encrypt(pad(plaintext))

print(plaintext)

print('')
print('')
print('')

print(ciphertext.decode('unicode_escape'))

print('')
print('')
print('')

decrypted = unpad(aes.decrypt(ciphertext))[blocksize//2:].decode('utf-8')

print(decrypted)