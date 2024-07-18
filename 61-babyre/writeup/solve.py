from subprocess import *

base = '0123456789abcdefghijklmnopqrstuvwxyz_{}'

# need sudo 
command = "perf stat -x : -e instructions:u ./babyre "

flag = 'hkcert21{'

start = 9

def max_dict(d):
    max = 0
    max_key = ""
    for t in d.keys():
        if d[t]>max:
            max = d[t]
            max_key = t 
    return max_key


for i in range(9,37):
    ctr_dict = {}
    input_flag = flag.ljust(37,'a')
    for p in base:
        input_flag = list(input_flag)
        input_flag[i] = p 
        input_flag = "".join(input_flag)
        target = Popen(command+input_flag, stdout=PIPE, stdin=PIPE, stderr=STDOUT, shell=True)
        target_output = target.communicate()
        instructions = int(str(target_output[0]).split(':')[0].replace('b\'Fail \\n',''))
        ctr_dict[p] = instructions
    curkey = max_dict(ctr_dict)
    flag+= curkey
    print(flag)



'''
from Crypto.Hash import MD5
import string

rol = lambda val, r_bits, max_bits=32: \
    (val << r_bits%max_bits) & (2**max_bits-1) | \
    ((val & (2**max_bits-1)) >> (max_bits-(r_bits%max_bits)))


flag = "hkcert21{h0p3_y0u_d1d_n07_r3ver53_1t}"

for i in range(0,len(flag)):
    h = MD5.new()
    h.update(flag[i].encode('utf-8'))
    cad = h.hexdigest()[24:]
    number = int(cad, 16)
    cal = (number * 0x0b6a) & 0xffffffff
    cal += i+1
    n = rol(cal,0x15)
    print(flag[i],'->',n)

'''
