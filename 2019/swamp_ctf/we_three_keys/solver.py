from m1z0r3 import *
from Crypto.Util.number import long_to_bytes,bytes_to_long

ip = "chal1.swampctf.com"
port = 1441


flag = ''
for i in range(1,4):
    s,f = sock(ip,port)
    print recv_until(f,'<= ') # choose key
    s.send('{}\n'.format(i)) # send i to choose i

    print recv_until(f,'<= ') # choose cmd
    s.send('1\n') # send 1 to choose enc

    print recv_until(f,'<= ') # ready to input

    ptext = hex(bytes_to_long('a'*32))[2:-1].zfill(64)
    s.send(ptext+'\n') # send ptext

    ctext1 = recv_line(f).strip() # get ciphertext
    ctext1_0 = ctext1[:32]

    print recv_until(f,'<= ') # choose cmd
    s.send('2\n') # send 2 to dec
    print recv_until(f,'<= ') # ready to input
    ct = ctext1_0 + '00'*16 + ctext1_0
    s.send(ct+'\n') # send to dec
    pt1 = recv_line(f).strip().decode('hex') # get pt
    print pt1
    pt1_0 = pt1[:16]
    pt1_2 = pt1[32:]
    print xor(pt1_0,pt1_2)
    flag += xor(pt1_0,pt1_2)
print flag
