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
