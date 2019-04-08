def egcd(a, b):
 if (a == 0):
     return [b, 0, 1]
 else:
     g, y, x = egcd(b % a, a)
     return [g, x - (b // a) * y, y]

def modInv(a, m):
 g, x, y = egcd(a, m)
 if (g != 1):
     raise Exception("[-]No modular multiplicative inverse of %d under modulus %d" % (a, m))
 else:
     return x % m
'''
'a'-->0
'z'-->26
Affine
encrypt
ax+b mod26

decrypt
modInv(a)(x-b)mod26
'''

def decrypt(m):
    return chr(11*(ord(j)-97-12)%26+97)
msg = 'myjdijfkwizq'
flag = ''.join([decrypt(i) for i in msg])
