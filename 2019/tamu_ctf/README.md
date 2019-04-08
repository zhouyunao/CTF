olver↓↓
```
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
```
最後ちょっとひねって、二文字のasciiを繋いだことに気づき、手動で分離しました。

## [Crypro 492pts] Holey Knapsack 
> My knapsack has a hole in it 

>Cipher text: 11b90d6311b90ff90ce610c4123b10c40ce60dfa123610610ce60d450d000ce61061106110c4098515340d4512361534098509270e5d09850e58123610c9
>Public key: {99, 1235, 865, 990, 5, 1443, 895, 1477}

ちょっとググったら、解説が発見
原理:https://nrich.maths.org/2199  
最初はprintableの文字を全部暗号化して辞書から当てようとしたら、うまくいかず。
たぶん昔が出題されたことあると踏んで検索したらありました。  
[https://github.com/everping/ctfs/blob/master/2015/4/plaidctf/crypto/lazy/solve.py:title]  
上記のsolver参考してやってみたけどもうまくいかず、最後ほかのメンバーが解いてくれました。  結局のところ、暗号文を分けないといけないですね。  


```
from sage.all import *
c = '11b90d6311b90ff90ce610c4123b10c40ce60dfa123610610ce60d450d000ce61061106110c4098515340d4512361534098509270e5d09850e58123610c9'
pubKey = [99, 1235, 865, 990, 5, 1443, 895, 1477]
nbit = len(pubKey)
c = [c[i:i+4] for i in range(len(c)-3,4)]
encoded = map(lambda x: int(x,16),c)
print "start"
for j in encoded:
    # create a large matrix of 0's (dimensions are public key length +1)
    A = Matrix(ZZ,nbit+1,nbit+1)
    # fill in the identity matrix
    for i in xrange(nbit):
        A[i,i] = 1
    # replace the bottom row with your public key
    for i in xrange(nbit):
        A[i,nbit] = pubKey[i]
    # last element is the encoded message
    A[nbit,nbit] = -j

    res = A.LLL()
    print "M: "
    M = res.row(8).list()
    print M
```
あとあと考えたらおそらく暗号化の実装がちょっと間違えたかな、二進数を逆転してから重りを計算したほうが多分ちゃんと辞書も作れると思います。

