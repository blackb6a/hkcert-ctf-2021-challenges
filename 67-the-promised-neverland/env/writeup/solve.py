#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from pwn import *
import requests
import binascii
import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
import hashlib
from gmpy2 import powmod
import itertools

from hash import SHA256

def connect():
    HOST = 'chalp.hkcert21.pwnable.hk'
    PORT = 28167

    context.log_level = 'debug'
    r = remote(HOST, PORT)
    return r

def spy(r, pbox, salt):
    r.sendlineafter('🤖 ', '🕵️')
    r.sendlineafter('😵 ', str(pbox))
    r.sendlineafter('🧂 ', base64.b64encode(salt))
    r.recvuntil('🔑 ')
    return binascii.unhexlify(r.recvline().strip())

def auth(r, password):
    r.sendlineafter('🤖 ', '🖥️')
    r.recvuntil('😵 ')
    pbox = eval(r.recvline())
    r.recvuntil('🧂 ')
    salt = base64.b64decode(r.recvline())
    
    permutated_password = password + salt + b'\x00'
    permutated_password = bytes([permutated_password[pbox[i]] for i in range(21)])
    hashed_password = hashlib.sha256(permutated_password).hexdigest()
    r.sendlineafter('🔑 ', hashed_password)

def solve_pow(challenge):
    i = 0
    while True:
        i += 1
        res = i.to_bytes(8, 'big')
        if hashlib.sha256(challenge + res).digest().startswith(b'\x00\x00\x00'):
            return res

# Note: If len(h_targets) == 16 and len(h_lookups) == 16, there is a ~65% chance that a pepper can be recovered.
def recover_pepper(h_targets, h_lookups):
    for h in h_targets:
        for i in range(256):
            s = SHA256(h)
            s.feed(bytes([i]) + b'\x80' + b'\x00' * 60 + b'\x02\x08')
            h_final = s.digest()

            if h_final not in h_lookups: continue
            return bytes([h_lookups.index(h_final)]), h
    return None

def attempt():
    r = connect()

    # Part 1. Solve PoW
    r.recvuntil('🔧 ')
    challenge = base64.b64decode(r.recvline())
    r.sendlineafter('🔩 ', base64.b64encode(solve_pow(challenge)))

    # Part 2. Solve the challenge

    # Remote (16 calls): hash([pw + NULL*4 + pepper])
    h_targets = set([
        spy(r, list(range(21)), b'\x00'*4)
        for _ in range(16)
    ])

    # Remote (16 calls): hash([pw + NULL*4 + fixed] && [pepper])
    h_lookups = [
        spy(r, list(range(16)) + [0x10, 0x10, 0x10, 0x10, 0x11, 0x12] + [0x10] * 41 + [0x13, 0x14], bytes([0, i, 0x80, 0xa8]))
        for i in range(16)
    ]

    # Local: Identify one of the pepper bytes
    res = recover_pepper(h_targets, h_lookups)
    if res is None:
        # --> Pepper byte not found, how sad.
        r.close()
        return False

    pepper, h_target = res

    charset = b'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'

    mapper = {}
    for suffix in itertools.product(charset, range(256)):
        s = SHA256(h_target)
        s.feed(bytes(suffix) + b'\x80' + b'\x00' * 59 + b'\x02\x10')
        h = s.digest()
        mapper[h] = bytes(suffix[:1])

    # Remote (16 calls): recover the password byte-by-byte
    password = b''
    for i in range(16):
        h_sub = spy(r, list(range(16)) + [0x10, 0x10, 0x10, 0x10, 0x11, 0x12] + [0x10] * 41 + [0x13, i, 0x14], b'\x00' + pepper + b'\x80\xa8')
        password_part = mapper.get(h_sub)
        assert password_part is not None
        password += password_part

    # Remote (1 call): sign in
    auth(r, password)
    print(r.recvline().strip())

    return True

def main():
    while not attempt(): pass

if __name__ == '__main__':
    global debug
    debug = 'debug' in os.environ

    main()