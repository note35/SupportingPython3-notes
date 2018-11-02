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
