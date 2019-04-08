n,e = (2531257, 43)

from Crypto.Util.number import long_to_bytes

'''
factor(2531257) = 509*4973
'''
p,q = (509,4973)

from Crypto.Util.number import inverse

phi = (p-1)*(q-1)
d = inverse(e,phi)
'''
d=58739L
'''
c = '906851 991083 1780304 2380434 438490 356019 921472 822283 817856 556932 2102538 2501908 2211404 991083 1562919 38268'.split(' ')
c = [int(i) for i in c]
import sys
for i in c:
    print pow(i,d,n)
msg = [103, 105, 103, 101, 109, 123, 83, 97, 118, 97, 103, 101, 95, 83, 105, 120, 95, 70, 108, 121, 105, 110, 103, 95, 84, 105,103, 101, 114, 115, 125]
for i in msg:
    sys.stdout.write(chr(i))

