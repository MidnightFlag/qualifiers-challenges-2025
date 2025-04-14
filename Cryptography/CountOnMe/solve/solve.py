from pwn import *
from Crypto.Util.Padding import pad, unpad

context.log_level = 'critical'

def oracle(inp):
    io.sendlineafter(b'enc=', inp.hex().encode())
    return b'good' in io.recvline()

def get_padding(position):
    padding = 16 - (position % 16)
    for guess in range(256):
        if guess == padding:
            continue
        test = bytearray(xor(flag_enc, known_content))
        test[position] ^= padding ^ guess
        for k in range(position + 1, position + padding):
            test[k] ^= padding
        if oracle(test[:position + padding]):
            return guess
    return None


io = remote('localhost', 1337)

io.recvuntil(b'CTR(flag)=')
flag_enc = bytes.fromhex(io.recvline().strip().decode())

known_content = bytearray([0] * len(flag_enc))

padding_len = get_padding(len(flag_enc) - 1)
known_content[-padding_len:] = bytearray([padding_len]*padding_len)

position = len(flag_enc) - 1 - padding_len
while position >= 0:
    result = get_padding(position)
    if result is None:
        break
    known_content[position] = result
    position -= 1

"""
☁  CTR  python3 solve.py
b'\x00CTF{PaddingOracleOnCTR}'

MCTF{PaddingOracleOnCTR}
"""