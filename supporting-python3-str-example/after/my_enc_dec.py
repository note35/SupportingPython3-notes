from builtins import chr  # pip install future

import sys

LIMITATION = 127

def encrypt(data, key):
    # data: bytes, key: bytes
    enc_d = b''
    for idx, d in enumerate(data):
        if sys.version_info >= (3,0):
            mixed = d + key[idx%len(key)]
        else:
            mixed = ord(d) + ord(key[idx%len(key)])
        enc_d = enc_d + chr(mixed%LIMITATION).encode('latin-1')
    return enc_d

def decrypt(data, key):
    # data: bytes, key: bytes
    dec_d = b''
    for idx, d in enumerate(data):
        if sys.version_info >= (3,0):
            mixed = d - key[idx%len(key)]
        else:
            mixed = ord(d) - ord(key[idx%len(key)]) 
        dec_d = dec_d + chr(mixed%LIMITATION).encode('latin-1')
    return dec_d
