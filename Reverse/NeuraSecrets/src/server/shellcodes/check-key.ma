pop rdi
movr rcx rdi
md5
movr rbx rax

genkeys
movr rdi rax
posthttp http://static1.midnighflag.fr:5000/pub
gethttp http://static1.midnightflag.fr:5000/pub
movr rdi rax
gensecret

gethttp http://static1.midnightflag.fr:5000/key
movr rdi rax
dec
movr rdi rax
cmp rax rbx
je 2
exit 1
readfile flag.txt.enc
movr rsi rcx
movr rdi rax
decfile
movr rdi rax
print
exit 0
