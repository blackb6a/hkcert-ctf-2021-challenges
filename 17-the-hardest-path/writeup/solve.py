#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from pwn import *
import hashlib
import base64
import time


def connect():
    # r = process(['python3', 'chall.py'])
    HOST = 'chalp.hkcert21.pwnable.hk'
    PORT = 28117

    context.log_level = 'debug'
    r = remote(HOST, PORT)
    return r

def solve_pow(challenge):
    i = 0
    while True:
        i += 1
        res = i.to_bytes(8, 'big')
        if hashlib.sha256(challenge + res).digest().startswith(b'\x00\x00\x00'):
            return res

def main():
    r = connect()

    # Part 1. Solve PoW
    r.recvuntil('🔧 ')
    challenge = base64.b64decode(r.recvline())
    r.sendlineafter('🔩 ', base64.b64encode(solve_pow(challenge)))
    r.sendlineafter('🥺 ', b'SSSSEENNEESSSSEENNEEEEEEEESSSSEESSSSWWSSSSEESSEESSSSWWSSSSWWWWWWSSWWSSSSSSEEEESSSSEESSEESSSSSSSSEENNEESSEEEESSEESSSSEESSEEEEEEEESSEEEESSSSEEEEEENNNNNNEENNWWNNEEEENNNNEEEENNEEEEEESSSSWWSSWWSSSSEEEESSWWSSEESSEEEESSSSEENNNNNNEEEESSEESSEESSEEEESSEENNEENNWWNNEEEEEESSEEEEEENNNNWWWWNNWWNNNNWWNNEEEEEENNEENNWWWWNNWWNNEENNEEEEEEEESSEESSEESSSSEESSEEEEEENNEESSSSSSEEEEEENNNNNNNNNNNNNNNNEEEEEEEEEEEESSEESSSSWWWWSSSSSSWWSSEESSEEEEEENNNNEESSEESSEEEENNEENNNNEEEEEENNEENNWWWWWWNNNNWWSSSSWWSSSSWWWWNNNNNNNNNNEENNEENNEENNEEEESSEESSSSEEEEEESSEEEEEEEENNNNEENNNNWWNNEEEENNNNEEEEEESSSSSSSSSSSSSSSSSSSSSSEESSSSEEEEEESSEESSWWSSSSEESSSSEEEENNEEEESSWWSSSSSSSSWWSSWWWWWWSSWWWWSSWWNNNNWWWWWWSSEESSWWSSWWSSEESSSSSSSSSSWWSSEEEESSSSSSEEEESSSSEESSEESSSSEEEESSEENNEEEESSSSWWSSEESSWWSSSSWWWWNNWWSSSSEESSEEEESSWWSSSSWWWWNNWWNNWWSSSSWWWWWWWWWWWWWWSSSSSSWWWWSSEESSWWSSWWWWWWSSWWWWWWWWSSSSEESSEEEEEESSSSSSEEEESSSSEEEEEESSWWWWSSSSSSSSSSSSEEEEEESSEEEENNEEEENNEEEENNEEEENNEEEESSEENNEEEESSSSSSSSWWSSWWSSSSWWSSSSSSEESSSSEEEESSEENNEESSEEEE')
    r.interactive()

if __name__ == '__main__':
    global debug
    debug = 'debug' in os.environ

    main()