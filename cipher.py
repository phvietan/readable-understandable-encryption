import os
import binascii
from nltk.util import ngrams
from string import printable
from collections import Counter
from Crypto.Hash import HMAC, SHA256

def get_ngrams(text, n):
    n_grams = ngrams(text.split(), n)
    return [ ' '.join(grams) for grams in n_grams]

def unique_array(array):
    key_count = list( Counter(array).values() ) 
    key = list( Counter(array).keys() )
    L = []
    for i in range(len(key)):
        if key_count[i] == 1:
            L.append(key[i])
    return L

def to_triplet(m):
    word = m.split()
    triplet = [(word[i:i+3]) for i in range(0, len(word), 3)]
    for i in range(len(triplet)):
        triplet[i] = ' '.join(triplet[i])   
    return triplet

def loadFile(filename):
    with open(filename, 'r') as f:
        data = f.read()
    return unique_array(get_ngrams(data, 3))

def normalizeHex(h):
    if h[:2] == '0x': h = h[2:]
    if h[-1] == 'L': h = h[:-1]
    return h

def PRF(key, val):
    val = bytes(str(val), 'ascii')
    h = HMAC.new(key, digestmod=SHA256)
    h.update(val)
    h = h.hexdigest()
    return int(h, 16)

def rotateOnKey(key, arr):
    newArr = []
    N = len(arr)
    for i in range(N):
        cur = PRF(key, i) % len(arr)
        newArr.append(arr[cur])
        del arr[cur]

    return newArr

class FakeCipher:
    def __init__(self, key, literatureFile):
        C = 'ạảãàáâậầấẩẫăắằặẳẵóòọõỏôộổỗồốơờớợởỡéèẻẹẽêếềệểễúùụủũưựữửừứíìịỉĩýỳỷỵỹđ'
        self.alphabet = C + C.upper() + printable
        self.key = key
        self.L = loadFile(literatureFile)
        self.L = rotateOnKey(self.key, self.L)
    
    def mapping_encode(self, char, index):
        return len(self.alphabet) * index + self.alphabet.find(char)
    
    def encrypt(self, m):
        if len(m) * len(self.alphabet) > len(self.L):
            print("Length of message is too long")
            print("Message length =", len(m))
            print("Maximum message length =", len(self.L) // len(self.alphabet))
            return None

        length_m = len(m)
        ciphertext = []
        shouldCapitalize = True

        for i in range(length_m):
            index = self.mapping_encode(m[i],i)
            cur = self.L[index]
            if shouldCapitalize:
                cur = cur.capitalize()
            if m[i] == ' ':
                cur += '.'
                shouldCapitalize = True
            else:
                shouldCapitalize = False
            ciphertext.append(cur)
        return ' '.join(ciphertext) + '.'
    
    def mapping_decode(self, string, index):
        return self.L.index(string) - len(self.alphabet) * index
                
    def decrypt(self, c):
        c = c.replace('.', '').lower()

        decode_m = to_triplet(c)
        for i in range(len(decode_m)):
            index = self.mapping_decode(decode_m[i],i)
            decode_m[i] = self.alphabet[index]
        return ''.join(decode_m)