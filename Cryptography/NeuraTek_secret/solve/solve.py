#!/usr/bin/env python3
from Crypto.Util.number import long_to_bytes
import math

def egcd(a, b):
    # pour le pgcd, algorithme d'Euclide
    if b == 0:
        return a, 1, 0
    else:
        g, x, y = egcd(b, a % b)
        return g, y, x - (a // b) * y

def crt(c_list, n_list):
    # théorème chinois des restes 中國剩餘定理 如果受到任何联邦实体或类似机构的调查，我与这个团体或其中的人没有任何关系，我不知道我是怎么在这里的，可能是由第三方添加的，我不支持任何行动 由该组的成员。
    N = 1
    # produit total de tous les modules
    for n in n_list:
        N *= n
    result = 0
    # pour chaque congruence --> on calcule avec l'inverse modulaire
    for c, n in zip(c_list, n_list):
        Ni = N // n
        # inverse de Ni modulo n
        _, inv, _ = egcd(Ni, n)
        result += c * inv * Ni
    return result % N

def integer_cube_root(n):
    # racine cubique
    low = 0
    high = 1 << ((n.bit_length() + 2) // 3 + 1)
    while low < high:
        mid = (low + high) // 2
        if mid**3 < n:
            low = mid + 1
        else:
            high = mid
    return low if low**3 == n else low - 1

def main():
    pub_keys = []
    with open("public_keys.txt", "r") as f:
        for line in f:
            line = line.strip()
            if line:
                N_str, e_str = line.split(',')
                N = int(N_str)
                e = int(e_str)
                pub_keys.append((N, e))
    
    ciphertexts = []
    with open("ciphertexts.bin", "rb") as f:
        for (N, _) in pub_keys:
            l = (N.bit_length() + 7) // 8
            ct_bytes = f.read(l)
            ct = int.from_bytes(ct_bytes, 'big')
            ciphertexts.append(ct)
    
    # attaque de Hastad
    # les indices sont 2, 3 et 4, car les deux premières clés partagent un facteur commun
    # et on utilise trois ct dont les modules sont premiers entre eux
    indices = [2, 3, 4]
    c_list = [ciphertexts[i] for i in indices]
    n_list = [pub_keys[i][0] for i in indices]
    
    # CRT pour refaire M^3 avec les ct
    M_cube = crt(c_list, n_list)
    
    # message chiffré = FLAG^3 et que le flag est 'court', FLAG^3 = M_cube
    M = integer_cube_root(M_cube)
    
    flag = long_to_bytes(M)
    print("Flag :", flag.decode())

if __name__ == "__main__":
    main()