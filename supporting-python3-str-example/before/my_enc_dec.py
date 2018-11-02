LIMITATION = 127

def encrypt(data, key):
    enc_d = ''
    for idx, d in enumerate(data):
        mixed = ord(d) + ord(key[idx%len(key)])
        enc_d = enc_d + unichr(mixed%LIMITATION)
    return enc_d

def decrypt(data, key):
    dec_d = ''
    for idx, d in enumerate(data):
        mixed = ord(d) - ord(key[idx%len(key)]) 
        dec_d = dec_d + unichr(mixed%LIMITATION)
    return dec_d
