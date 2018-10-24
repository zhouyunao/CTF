import os, base64, time, random, string
from Crypto.Cipher import AES
from Crypto.Hash import *

asciimap = string.ascii_letters+string.digits
proof4after = raw_input('Give the proof4after:')
digest = raw_input('Give the hexdigest:')



def test(proof4after,digest):
    flag = 0
    for c0 in asciimap:
        for c1 in asciimap:
            for c2 in asciimap:
                for c3 in asciimap:
                    print c0+c1+c2+c3
                    if SHA256.new(c0+c1+c2+c3+proof4after).hexdigest() == digest:
                        print 'Bingo'
                        return c0+c1+c2+c3
start=time.time()
ans = test(proof4after,digest)
print ans
end = time.time()
print end-start
