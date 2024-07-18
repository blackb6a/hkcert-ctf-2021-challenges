# Idea
# "ark secret"
# "sb data 000...00"
# "sb secret"
# 255 calls to "mc data XY...XY"
# "mc secret"

import itertools
from pwn import *
from tqdm import tqdm
from Crypto.Cipher import AES as RealAES

from aes import AES

no_op = lambda *x: None

key = [None for _ in range(16)]

# r = process(['python3', 'chall.py'])
r = remote('chalp.hkcert21.pwnable.hk', 28207)

r.recvuntil(b'Hey. This is the encrypted flag you gotta decrypt: ')
c_flag = bytes.fromhex(r.recvuntil(b'.')[:-1].decode())

# [*] 1 oracle call
r.sendlineafter(b'> ', 'ark secret')
c = bytes.fromhex(r.recvline().decode())

cipher = AES(b'\0'*16)
cipher._add_round_key = no_op
m = cipher.decrypt(c)
assert m[0::4] == m[1::4] == m[2::4] == m[3::4]
key[0:4] = m[0::4]

# [*] +2 oracle calls (3 in total)
r.sendlineafter(b'> ', 'sb data 00000000000000000000000000000000')
c0 = bytes.fromhex(r.recvline().decode())
r.sendlineafter(b'> ', 'sb secret')
c1 = bytes.fromhex(r.recvline().decode())
cipher = AES(b'\0'*16)
cipher._add_round_key = no_op
cipher._inv_sub_bytes = no_op
m = cipher.decrypt(xor(c0, c1))
assert m[0::4] == m[1::4] == m[2::4] == m[3::4]
key[4:8] = m[0::4]

# [*] +65 oracle calls (70 in total)
cs = []
for i in range(64):
    m = bytes([4*i + j%4 for j in range(16)])
    r.sendlineafter(b'> ', f'mc data {m.hex()}')
    c = bytes.fromhex(r.recvline().decode())
    c = bytes([c[9*k%16] for k in range(16)]) # Rearrange so that m[i] will affect c[i] instead of c[9i mod 16]
    cs.append(c)

r.sendlineafter(b'> ', 'mc secret')
c = bytes.fromhex(r.recvline().decode())
c = [c[9*i%16] for i in range(16)]

# This is the last four bytes of the key
for i in range(64):
    for j in range(16):
        if cs[i][j] != c[j]: continue
        key[12 + j//4] = 4*i + j%4


# [*] +58 oracle calls (128 in total)
# Try to reduce the search space by 30% (or even more if there is a match)
cs = []
for i in range(57):
    m = bytes([i])*16
    r.sendlineafter(b'> ', f'sr data {m.hex()}')
    c = bytes.fromhex(r.recvline().decode())
    cs.append(c)

r.sendlineafter(b'> ', 'sr secret')
c = bytes.fromhex(r.recvline().decode())

matched = 0
candidates = [list(range(57, 256)) for _ in range(4)]
for i in range(57):
    for j in range(4):
        if cs[i][4*j:4*j+4] != c[4*j:4*j+4]: continue
        candidates[j] = [i]
        matched += 1

total = (256-57)**(4-matched)
print(f'{matched}/4 bytes matched (the more the better). Need to search {total} AES keys.')

for subkey in tqdm(itertools.product(*candidates), total=(256-57)**(4-matched)):
    key[8:12] = subkey
    cipher = RealAES.new(bytes(key), RealAES.MODE_ECB)
    m = cipher.decrypt(c_flag)
    if not m.startswith(b'hkcert21{'): continue
    print(f'The flag is found! {m}')
    break