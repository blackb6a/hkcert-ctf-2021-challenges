import re
from Crypto.Util import Counter
from Crypto.Cipher import AES
import os

def xor(a, b):
    return bytes([u^^v for u, v in zip(a, b)])

#                      C o n g r a t u l a t i o n s ! _ h k c e r t 2 1 {                                                                       }
known = bytes.fromhex('ffffffffffffffffffffffffffffffffffffffffffffffffffff8080808080808080808080808080808080808080808080808080808080808080808080ff')
m =     bytes.fromhex('436f6e67726174756c6174696f6e732120686b6365727432317b00000000000000000000000000000000000000000000000000000000000000000000007d')
c =     bytes.fromhex('6ccb80c46c19243a37633d316a66871ca70ec8a44f48a80134f31d8d27f920c6bd5d810831833221d0f282130d2c222de38c2080ef995b2ad10dc5af8518')

keystreams = []
for k in range(256):
    cipher = AES.new(bytes([k]) + b'\0'*15, AES.MODE_CTR, counter=Counter.new(128, initial_value=int(0)))
    keystreams.append(
        cipher.encrypt(b'\0'*len(c))
    )

A = []
b = []

for i, (rc, mc, cc) in enumerate(zip(known, m, c)):
    for j in range(8):
        if (rc>>j) & 1 == 0: continue
        mb = (mc>>j) & 1
        cb = (cc>>j) & 1

        row = [(k[i]>>j) & 1 for k in keystreams]

        A.append(row)
        b.append(mb^^cb)

F = GF(2)
A = Matrix(F, A)
b = vector(F, b)

print(f'Expecting {2**(A.ncols() - A.rank())} candidates to be guessed ({A.ncols()} unknowns vs {A.nrows()} equations)')

x0 = A.solve_right(b)
for dx in A.right_kernel():
    x = x0+dx

    flag = c
    for k, xc in zip(keystreams, x):
        if xc == 0: continue
        flag = xor(flag, k)
    flag = flag.decode()
    if not re.match(r'Congratulations! hkcert21\{\w+\}', flag): continue
    print(f'[*] Flag recovered: {flag}')