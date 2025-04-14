A = 7
B = 3
M = 39
XOR_KEY = 0x66

# Calcul inverse modulaire
def modinv(a, m):
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    raise ValueError(f"No modinv for {a} mod {m}")

A_INV = modinv(A, M)

# Base 39 alphabet
alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ{}_"

def val_to_char(v):
    if 0 <= v < len(alphabet):
        return alphabet[v]
    raise ValueError(f"Invalid value: {v}")


# Déchiffrement
def decrypt_val(y):
    aff = y ^ XOR_KEY
    val = (A_INV * (aff - B)) % M
    return val_to_char(val)

def decrypt_flag(enc_list):
    return ''.join(decrypt_val(x) for x in enc_list)

if __name__ == "__main__":
    cipher = [103, 111, 109, 120, 115, 66, 114, 69, 108, 98, 69, 109, 99, 126, 69, 110, 126, 70, 69, 66, 118, 108, 122]
    decrypted = decrypt_flag(cipher)
    print("Decrypted:", decrypted)
