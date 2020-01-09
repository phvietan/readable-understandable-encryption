import os
import json
from cipher import FakeCipher

js = {}
with open('options.json', 'r') as f:
    js = json.load(f)

key = os.urandom(32)
wordlist = js["crawl_output"]

cipher = FakeCipher(key, wordlist)

message = 'Nạp cho tôi 20k. Password là alo123 nha!'
print("Message =", message)
############################################

c = cipher.encrypt(message)
print("Ciphertext =", c)
############################################

decrypted = cipher.decrypt(c)
print("Decrypted ciphertext =", decrypted)
############################################
