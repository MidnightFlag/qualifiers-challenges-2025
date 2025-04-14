from Crypto.Cipher import AES
from Crypto.Util import Counter
from Crypto.Util.Padding import pad, unpad
from Crypto.Util.number import bytes_to_long
import os

class CTR:
    def __init__(self):
        self.key = os.urandom(16)

    def encrypt(self, pt):
        iv = os.urandom(16)
        ctr = Counter.new(128, initial_value=bytes_to_long(iv))
        cipher = AES.new(self.key, AES.MODE_CTR, counter=ctr)
        enc = iv + cipher.encrypt(pad(pt, 16))
        return enc

    def decrypt(self, ct):
        try:
            ctr = Counter.new(128, initial_value=bytes_to_long(ct[:16]))
            cipher = AES.new(self.key, AES.MODE_CTR, counter=ctr)
            dec = unpad(cipher.decrypt(ct[16:]), 16)
            return dec
        except Exception:
            return False

if __name__ == "__main__":
    cipher = CTR()
    flag = os.getenv('FLAG', 'MCTF{ThisIsAFakeFlag}').encode()
    ct = cipher.encrypt(flag)
    print(f"CTR(flag)={ct.hex()}")
    while 1:
        enc = bytes.fromhex(input("enc="))
        dec = cipher.decrypt(enc)
        if bool(dec) or dec == flag:
            print('Look\'s good')
        else:
            print('Hum,this is a weird input')
