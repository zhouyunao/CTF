import math
from sets import Set
from Crypto.Util.number import *
from hashlib import md5
import itertools
from Crypto.Hash import *

# By Harry
private = 8213242002076053911181908692341986030919593545361549673265676083814813944695092587591375250L
primes = [2,5,5,5,19,79,239,106979,206603,63634387,35183414437,1643759635229,23644671381761,26047344042803,1828083256178279]

p = 1
for i in primes:
    p *= i
assert p == private

md5 = Set([])
for i in range(len(primes)):
    for x in itertools.combinations(primes,i):
        d = 0
        for item in x:
            d += math.log(item,2)
        if d > 120 and d <= 128:
            product = 1
            for item in x:
                product *= item
            md5.add(product)
print len(md5)
# By Samuel
q = [0] * 27
def solve(n, l, x):
    global q
    if l == 27:
        m = "".join(q[l - 1 : : -1])
        hash = MD5.new()
        hash.update(m)
        if n == 0 and int(hash.digest().encode('hex'), 16) == x:
            print 'm1z0r3{%s}' % m
        return
    for i in range(32, 128):
        if n % i == 0:
            q[l] = chr(i)
            solve(n / i - 1, l + 1, x)

for x in md5:
    solve(private / x, 0, x)
