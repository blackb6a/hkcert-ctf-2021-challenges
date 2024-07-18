from pwn import *
from tqdm import tqdm
import base64        
from functools import reduce
from gmpy2 import iroot
from Crypto.Cipher import AES

# Copied and simplified from https://rosettacode.org/wiki/Chinese_remainder_theorem#Python_3.6
def chinese_remainder(n, a):
    sum = 0
    prod = reduce(lambda a, b: a*b, n)
    for n_i, a_i in zip(n, a):
        p = prod // n_i
        sum += a_i * pow(p, -1, n_i) * p
    return sum % prod
 

class Challenge:
    def __init__(self):
        self.r = remote('chalp.hkcert21.pwnable.hk', 28157)
    
    def send(self, m):
        self.r.sendlineafter(b'[cmd] ', f'send {format(m, "x")}')
        return int(self.r.recvline().strip().decode(), 16)

    def pkey(self):
        self.r.sendlineafter(b'[cmd] ', 'pkey')
    
    def backup(self):
        self.r.sendlineafter(b'[cmd] ', 'backup')
        return int(self.r.recvline().strip().decode(), 16)

    def flag(self):
        self.r.sendlineafter(b'[cmd] ', f'flag')
        return bytes.fromhex(self.r.recvline().decode())


def solve():

    ns = []
    cs = []

    c = Challenge()
    for i in range(5):
        c.pkey()
        n = c.send(-1) + 1
        c0 = c.backup()
        ns.append(n)
        cs.append(c0)

    k17 = chinese_remainder(ns, cs)
    N   = reduce(lambda a, b: a*b, ns)
    
    k, ok = iroot(k17, 17)
    assert ok
    k = int(k)
    k = int.to_bytes(k, 32, 'big')

    c0 = c.flag()

    cipher = AES.new(k, AES.MODE_CBC, b'\0'*16)
    flag = cipher.decrypt(c0)
    print(flag)


solve()