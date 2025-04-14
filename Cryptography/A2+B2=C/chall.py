from sage.all import randint, next_prime
from Crypto.Util.number import bytes_to_long

class RSA:
    def __init__(self, hb, lb) -> None:
        self.hb = hb
        self.lb = lb
        self.u1 = randint(0, 2**30)
        self.u2 = randint(0, 2**30)
        self.keygen()
    
    def keygen(self) -> None:
        self.base = randint(2**self.hb-1, 2**self.hb)
        self.e = 0x10001
        self.p = next_prime(self.u1*self.base + randint(2, 2**self.lb))
        self.q = next_prime(self.u2*self.base + randint(2, 2**self.lb))
        self.n = self.p * self.q

    def sum(self):
        return self.u1**2 + self.u2**2

    def encrypt(self, m: bytes) -> int:
        m_ = bytes_to_long(m)
        c = pow(m_, self.e, self.n)
        return c
    

rsa = RSA(
    hb=2048,
    lb=256
)
print(f"c0 = {rsa.sum()}")
print(f"c1 = {rsa.encrypt(b'MCTF{ThisIsAFakeFlag}')}")
print(f"c2 = {rsa.encrypt(b'Lorem Ipsum is simply dummy text of')}")
print(f"c3 = {rsa.encrypt(b'the printing and typesetting industry')}")
 