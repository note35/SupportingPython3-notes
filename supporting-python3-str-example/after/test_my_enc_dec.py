from my_enc_dec import encrypt, decrypt

KEY = b'small_key'

def test_encrypt():
    assert encrypt(b'cat', KEY) == b'WOV'
    assert encrypt(b'dog', KEY) == b'X]I'

def test_decrypt():
    assert decrypt(b'WOV', KEY) == b'cat'
    assert decrypt(b'X]I', KEY) == b'dog'

test_encrypt()
test_decrypt()
