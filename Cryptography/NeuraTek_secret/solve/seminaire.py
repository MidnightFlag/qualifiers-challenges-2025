from Crypto.Util.number import getPrime, bytes_to_long
import math
from oh import FLAG

public_keys = []
private_keys = []

p = getPrime(512)
q1 = getPrime(512)
q2 = getPrime(512)
N1 = p * q1
N2 = p * q2
public_keys.extend([(N1, 3), (N2, 3)])
private_keys.extend([(p, q1), (p, q2)])

for _ in range(8):
    p = getPrime(512)
    q = getPrime(512)
    N = p * q
    public_keys.append((N, 3))
    private_keys.append((p, q))

ciphertexts = [pow(bytes_to_long(FLAG), 3, N) for N, _ in public_keys]

with open("public_keys.txt", "w") as f:
    for N, e in public_keys:
        f.write(f"{N},{e}\n")

with open("ciphertexts.bin", "wb") as f:
    for ct in ciphertexts:
        f.write(ct.to_bytes((ct.bit_length() + 7) // 8, 'big'))