#!/usr/bin/python3
#key = 0xXXXXXXXXXXXXX
key = 0x1111111111111
size = len(bin(key)[2:])
print ('length:{}'.format(size))
def F(left, right, key):
    newR = (((right^key)>>3) + (((right^key)&7)<<(size//2-3))) ^ 0x3ffffff
    return (right, left^newR)

def encrypt(block, key):
    key0 = key>>size//2   # 上位ビット
    key1 = key & int('1'*(size//2),2)  # 下位ビット
    print ('[-]key0:{}'.format(int(key0)))
    print ('[-]key1:{}'.format(int(key1)))
    L = block>>size//2                # 上位ビット
    R = block & int('1'*(size//2),2)  # 下位ビット
    print ('[-]right:{}'.format(R))
    print ('[-]left:{}'.format(L))
    for i in range(128):
        L,R = F(L,R,key0)
        print ('{0}----{1}'.format(L,R))
        L,R = F(L,R,key1)
        print ('{0}----{1}'.format(L,R))
        if i == 127:
            print ('{0}----{1}'.format(L,R))

    return (L<<size//2)+R

while True:
    pt = int(input("Enter a block of plaintext (as hex, at most 13 chars) that you would like to encrypt: ")[:13],16)
    ct = encrypt(pt,key)
    print (ct)
    print("Here is the ciphertext:", (hex(ct)[2:]).zfill(size//4))
