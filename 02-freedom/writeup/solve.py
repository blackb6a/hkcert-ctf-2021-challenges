from pwn import *

context.log_level = 'debug'

def xor(a, b):
    return bytes([u^v for u, v in zip(a, b)])

# r = process(['python3', 'chall.py'])
r = remote('chalp.hkcert21.pwnable.hk', 28102)

r.sendlineafter(b'> ', 'cbc data ' + '00'*80)
c1 = bytes.fromhex(r.recvline().strip().decode())
r.sendlineafter(b'> ', 'ofb flag')
c2 = bytes.fromhex(r.recvline().strip().decode())

print(xor(c1, c2))
