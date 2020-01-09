# About

Normal encryption algorithms like 3-DES or AES indeed hide the original message from any eavesdropper along the network traffic. However, do you truly believe that those encryption algorithms have not been cracked by NSA, CIA, FBI,...? For this repo, I introduce another way to encrypt messages using symmetric encryption.

# Feature

Using the encryption algorithm I implement here, people can read (and somewhat understand) the ciphertext. But actually it does not have meaning at all.

# Challenging problems

It is very hard to share the secret key between 2 individuals. For this repo I assume that both parties hold some previous knowledge with each other. Then using the previous knowledge, the 2 parties can encrypt and communicate with each other.

# Prerequisite
Use pip3 to install: bs4, lxml, requests, pycrypto, nltk

# Run code:

Please use python3 to run code.

Encrypting and decrypting files
```bash
  python3 main.py
```

Evaluating results
```bash
  python3 evaluate.py
```