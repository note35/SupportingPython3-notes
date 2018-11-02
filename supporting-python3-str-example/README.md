# Supporting Python3: Str Example

Supporting Python3 has too many prerequisites, the most painful one is str. This page is targeted to reduce the effort on learn those thing.

## Basic Concept
- python2: default str `''` is bytes, `u''` is text(unicode)
- python3: default str `''` is text, `b''` is bytes
  - The text and bytes can only be equivalent in both versions if they use same encode/decode.
  - If you can assure the all given character are limited in `ascii` encode, bytes is equivalent to text.
- bytes and text can be inter-converted:
  - text to bytes: some_text.encode(encode)
  - bytes to text: some_bytes.decode(encode)
    - encode can be `latin-1`, `utf-8`, `ascii`...etc

## Supporting Python3 Strategy
Knowing the default behavior between python2 and python3 are totally inverse, following below steps can make your life easier. I won't call it best practice, but at least it's a followable practice.

*Note: The definition of transition period: before all packages can be written in python3 ONLY.*

### During transition period

- Address `u''` and `b''` strictly for all '' (Actually, many python built-in functions work by giving `''` in python2/3)

- Check all the string in the package, including all arguments and returns of functions.
   - Add doc string or type[PEP484](https://www.python.org/dev/peps/pep-0484/#suggested-syntax-for-python-2-7-and-straddling-code) to indicate `byte/text` strictly
   - You must find some incompatible code between python2/3, meantime, make the code with original(python2) behavior by using `sys.version_info >= (3,0)` or `six.PY3`, see example below.
     - six/future are recommended in large project
- Run and pass unit tests (Update unit tests by above work too)
- Run and pass depending tools, and test them in production environment

### After transition

- Add `from __future__ import [unicode_literals](https://python-future.org/unicode_literals.html)` to prevent future code modification with unclear `''` (without `b''` or `u''`), all code should have python3 behavior in any case AFTER the supporting work.


### Tips

[Source](https://www.youtube.com/watch?v=elAV6aZDMvg)

- Use unicode for text data
  - Standard library of python2 accepts both text(unicode) and bytes.
  - Standard library of python3 accepts only only text. (Exception: file system paths)
- Text inside the system is text(unicode)
  - Decode bytes to text as soon as possible
  - Encode text to bytes as late as possible
- Visualize the system design to understand text related  function I/O and system I/O
  - Do not allow IO accept both bytes/text (Exception: file system paths)
- Others
  - Use from __future__ for every files to make python2 code behavior like python3.
  - Use six and future for large project

## Example

Assume we have a python27 only package, and now your mission is supporting python3 and keeping python27 functionality.

```
.
├── my_enc_dec.py
├── run_crypto.py
└── test_my_enc_dec.py
```

**my_enc_dec.py**
```python
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
```

**test_my_enc_dec.py**

```python
from my_enc_dec import decrypt, encrypt

KEY = 'small_key'

# test encrypt
assert encrypt('cat', KEY) == 'WOV'
assert encrypt('dog', KEY) == 'X]I'

# test decrypt
assert decrypt('WOV', KEY) == 'cat'
assert decrypt('X]I', KEY) == 'dog'
```

**run_crypto.py**

```python
#!/usr/bin/env python

import argparse
import sys
from my_enc_dec import decrypt, encrypt

parser = argparse.ArgumentParser()
parser.add_argument('-f', dest='funct', required=True, choices=['dec', 'enc'])
parser.add_argument('-k', dest='key', required=True)
args = parser.parse_args()

data = sys.stdin.read()
if args.funct == 'enc':
    sys.stdout.write(encrypt(data, args.key))
if args.funct == 'dec':
    sys.stdout.write(decrypt(data, args.key))
```

**People can run command as below:**
dec
```bash
$ echo foo | python2.7 run_crypto.py -f enc -k my_key | python2.7 run_crypto.py -f dec -k my_key
$ foo
```

### First Try

The example can work after adding `builtins.chr`

```python
from builtins import chr

LIMITATION = 127

def encrypt(data, key):
    enc_d = ''
    for idx, d in enumerate(data):
        mixed = ord(d) + ord(key[idx%len(key)])
        enc_d = enc_d + chr(mixed%LIMITATION)
    return enc_d

def decrypt(data, key):
    dec_d = ''
    for idx, d in enumerate(data):
        mixed = ord(d) - ord(key[idx%len(key)]) 
        dec_d = dec_d + chr(mixed%LIMITATION)
    return dec_d
```

It seems works?

```bash
$ echo foo | python3.6 run_crypto.py -f enc -k my_key | python3.6 run_crypto.py -f dec -k my_key
$ foo
```

However, it can be wrong when giving bytes string with non-ascii encode.

(Note: I meaningfully make unit test not cover this, because you might meet this when altering some package without proper unit tests.)

```bash
$ python -c 'print "\x80\x1e\x00\x00"' | python2.7 run_crypto.py -f enc -k my_key | python2.7 run_crypto.py -f dec -k my_key

$ python -c 'print "\x80\x1e\x00\x00"' | python3.6 run_crypto.py -f enc -k my_key | python3.6 run_crypto.py -f dec -k my_key
Traceback (most recent call last):
  File "run_crypto.py", line 12, in <module>
    data = sys.stdin.read()
  File "/usr/local/Cellar/python3/3.6.2/Frameworks/Python.framework/Versions/3.6/lib/python3.6/codecs.py", line 321, in decode
    (result, consumed) = self._buffer_decode(data, self.errors, final)
UnicodeDecodeError: 'utf-8' codec can't decode byte 0x80 in position 0: invalid start byte
```

### Root Cause

#### Why is wrong?
A. Because the I/O weren't fully tested.

#### Looking at run_crypto.py, what is the meaning of str in input: `sys.stdin.read()` and output of `sys.stdout.write()`?

- In python2.x:
  - `sys.stdin.read()` is bytes
  - `sys.stdout.write()` is bytes 
- In python3.x:
  - `sys.stdin.read()` is text
  - `sys.stdout.write()` is text
  - `sys.stdin.buffer.read()` is bytes
  - `sys.stdout.buffer.read()` is bytes
 
#### what's the type of those "str" arguments in the command?
- In python2.x: bytes
- In python3.x: text

### Proper Try

If you have known all given bytes string in python2 are limited to `ascii` encode, you have finished the work. But if this assumption is wrong, then you will need following modifications.

Knowing the difference of IO behavior, let's handle it first.

**run_crypto.py**
```python
#!/usr/bin/env python

import argparse
import sys
from my_enc_dec import decrypt, encrypt

parser = argparse.ArgumentParser()
parser.add_argument('-f', dest='funct', required=True, choices=['dec', 'enc'])
parser.add_argument('-k', dest='key', required=True)
args = parser.parse_args()

if sys.version_info >= (3,0):
    data = sys.stdin.buffer.read()
    if args.funct == 'enc':
        sys.stdout.buffer.write(encrypt(data, args.key.encode('latin-1')))
    if args.funct == 'dec':
        sys.stdout.buffer.write(decrypt(data, args.key.encode('latin-1')))
else:
    data = sys.stdin.read()
    if args.funct == 'enc':
        sys.stdout.write(encrypt(data, args.key))
    if args.funct == 'dec':
        sys.stdout.write(decrypt(data, args.key))
```

Ooops, it's not working in python3

Obviously, the function input is expected to be text in python3, but it is bytes in python2. Let's alter the entire library now.

```bash
$ python -c 'print "\x80\x1e\x00\x00"' | python2.7 run_crypto.py -f enc -k my_key | python2.7 run_crypto.py -f dec -k my_key

$ python -c 'print "\x80\x1e\x00\x00"' | python3.6 run_crypto.py -f enc -k my_key | python3.6 run_crypto.py -f dec -k my_key
Traceback (most recent call last):
  File "run_crypto.py", line 17, in <module>
    sys.stdout.buffer.write(decrypt(data, args.key))
  File ".../my_enc_dec.py", line 15, in decrypt
    mixed = ord(d) - ord(key[idx%len(key)]) 
TypeError: ord() expected string of length 1, but int found
Traceback (most recent call last):
  File "run_crypto.py", line 15, in <module>
    sys.stdout.buffer.write(encrypt(data, args.key))
TypeError: a bytes-like object is required, not 'str'
```

**my_enc_dec.py**
(Note: `ord` is not needed for python3, `chr` needs to be converted)

```
from builtins import chr

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
```

Don't forget to update the unit test.

**test_my_enc_dec.py**

```python
from my_enc_dec import encrypt, decrypt

KEY = b'small_key'

# test encrypt():
assert encrypt(b'cat', KEY) == b'WOV'
assert encrypt(b'dog', KEY) == b'X]I'

# test decrypt():
assert decrypt(b'WOV', KEY) == b'cat'
assert decrypt(b'X]I', KEY) == b'dog'
```

Finally, after supporting python3, add `from __future__ import unicode_literals` to all python files to prevent future confusion. *It's optional, but I recommend.*

Now, you script works as expected, your unit test is also passed!

```bash
$ python -c 'print "\x80\x1e\x00\x00"' | python2.7 run_crypto.py -f enc -k my_key | python2.7 run_crypto.py -f dec -k my_key

$ python -c 'print "\x80\x1e\x00\x00"' | python3.6 run_crypto.py -f enc -k my_key | python3.6 run_crypto.py -f dec -k my_key
```
