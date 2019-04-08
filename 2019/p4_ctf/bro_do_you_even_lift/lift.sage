flag = int(open('flag.txt','r').read().encode("hex"),16)
# flag = int('p4{fffffffffffffffffffffff}'.encode("hex"),16)
ranges = int(log(flag,2))
p = next_prime(ZZ.random_element(2^15, 2^16))
k = 100
N = p^k
d = 5
P.<x> = PolynomialRing(Zmod(N), implementation='NTL')
pol = 0
for c in range(d):
    pol += ZZ.random_element(2^ranges, 2^(ranges+1))*x^c
print(pol)
remainder = pol(flag)
print(remainder)
pol = pol - remainder
print(pol(flag))
assert pol(flag) == 0

print(p)
print(pol)
