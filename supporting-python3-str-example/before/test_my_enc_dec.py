from my_enc_dec2 import encrypt, decrypt

KEY = 'small_key'

def test_encrypt():
    assert encrypt('cat', KEY) == 'WOV'
    assert encrypt('dog', KEY) == 'X]I'

def test_decrypt():
    assert decrypt('WOV', KEY) == 'cat'
    assert decrypt('X]I', KEY) == 'dog'

test_encrypt()
test_decrypt()
