from Crypto.PublicKey import RSA
from flag import flag

assert(flag.startswith("KOSENCTF"))

m = int(flag.encode("hex"), 16)
key = RSA.generate(2048, e=3)

while pow(m, key.e) < key.n:
    m = m << 1

c = pow(m, key.e, key.n)
print("c={}".format(c))
print("e={}".format(key.e))
print("n={}".format(key.n))
