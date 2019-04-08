# 89 50 4E 47 0D 0A 1A 0A 00 00 00 0D
# 18 9a 6d 45 89 a2 9c 4e
import struct

M = pow(2,32)
def lcg(m, a, c, x):
	return (a*x + c) % m

def encrypt(e,d,x,m,a,c):
    for i in range(len(d)):
	    e += struct.pack('>I', x ^ struct.unpack('>I', d[i])[0])
	    x = lcg(m, a, c, x)
    return e

# def decrypt(e,d,x):
#     return encrypt(e,d,x)

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


knownpt = '\x89\x50\x4E\x47\x0D\x0A\x1A\x0A\x00\x00\x00\x0D\x49\x48\x44\x52'
ct = ''
ct_full = ''

with open('flag.png.enc','rb') as f:
    ct_full = f.read()
    ct = ct_full[:16]
assert(ct == ct_full[:16])
# print ct_full
recgamma = ''.join([chr(d ^ c) for d,c in zip(map(ord, knownpt), map(ord, ct))])

states = []
ct_block = []
pt_block = []
for i in range(0,len(ct),4):
    states.append(struct.unpack('>I',recgamma[i:i+4])[0])

print states

# subtract eq. 0 from 1 and 2
x = states[1]-states[2]
alpha = states[0]-states[1]

y = states[1]-states[3]
beta = states[0]-states[2]
print alpha,beta
# recover a, b
# g, p, q = egcd(alpha, M)
# g2, p2, q2 = egcd(beta, M)
#
# if(g == 1):
#   mod_inv = p % M
#   a = (x * mod_inv) % M
# elif(g2 == 1):
#   mod_inv = p2 % M
#   a = x * mod_inv % M
# else:
#   print "[-]No modular multiplicative inverse found :("
#   exit()

a = (y * modInv(beta,M)) % M

b = states[1]-(states[1-1]*a) % M
# inverse of a
# g, p, q = egcd(a, M)
# a_inv = modInv(a,M)
init_state = states[0]

# Recover LCG
print "[+]Recovered LCG(a=%d, b=%d, init=%d)" % (a, b, init_state)
ct_block = [ct_full[i:i+4] for i in range(0, len(ct_full), 4)]
decrypted = ''
print len(ct_block)
decrypted = encrypt(decrypted,ct_block,init_state,M,a,b)

f = open('flag.png','wb')
f.write(decrypted)
f.close()

print "[+]Done!"
