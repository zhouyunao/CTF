from Crypto.Util.number import *
from Crypto.Random.random import randint
import gmpy
import os
import key

def gen_key(bits=1024):
  while True:
    p = getPrime(bits)
    q = getPrime(bits)
    if p != q and gmpy.gcd(p*q, (p-1)*(q-1)) == 1:
      break
  n = p*q
  return n,(p,q)

e = 4919

while True:
  n,(p,q) = gen_key()
  phi = (p-1)*(q-1)
  d = gmpy.invert(e,phi)
  if e*d%phi == 1:
    break

print "n =",n

def encrypt1(a,b):
  s = getPrime(4)
  c = pow(n+b,a,n**(s+1))
  return c

def encrypt2(m):
  assert m < n
  c = pow(m,e,n)
  assert pow(c,d,n) == m
  return c

a = key.a
b = key.b

FLAG = key.FLAG
while len(FLAG) * 8 < 2048:
  FLAG += os.urandom(1)
FLAG = FLAG[:-2]
m = bytes_to_long(FLAG)

enc1 = encrypt1(a,b)
print "enc1 =",enc1

enc2 = encrypt2(m+a)
enc3 = encrypt2(m+b)
print "enc2 =",enc2
print "enc3 =",enc3
