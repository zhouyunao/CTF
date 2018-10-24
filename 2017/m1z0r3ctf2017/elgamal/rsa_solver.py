# coding:utf-8
#!/usr/bin/python2

import socket
from sys import exit
import SocketServer
from Crypto.Util.number import *
from Crypto.Util.number import bytes_to_long as b2l
from Crypto.Util.number import long_to_bytes as l2b
from random import randint
# ===========read until==================
def read_until(f, delim='\n'):
    data = ''
    while not data.endswith(delim):
        data += f.read(1)
    return data



# ======== Extended Euclidean algorithm ========
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

# ======== mod inverse ========
def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m
# ===================Dec======================

def dec(y,g,p,c1,c2):
    x = 0
    while True:
        m = (pow(modinv(c1,p),x,p) * c2) % p
        b_m = l2b(m)
        x += 1
        if b_m.startswith('m1z0r3{'):
            print b_m
            break

def sock(remoteip, remoteport):
# --- meke the socket ---
# --- AF_INET->internet socket
# --- SOCK_STREAM->TCP BTW SOCK_DGRAM->UDP
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((remoteip, remoteport))
    return s, s.makefile('rw', bufsize=0)



remotehost = "13.113.218.1 "
# remotehost = "192.168.0.4"
remoteport = 54321
s,f = sock(remotehost,remoteport)


def main():
    # c1 = long(raw.input())
    # c2 = long(raw.input())
    # line = map(long,raw.input().split(','))
    # y = line[0]
    # g = line[1]
    # p = line[2]
# ============= skip the menu =========#
    menu = read_until(f,"> ")
    print menu
# ============= command 3,4 get m1 and pk1=============#
    s.send('3\n')
    enc_flag = read_until(f,'-').strip()
    enc_flag = enc_flag[enc_flag.find(':')+1:-1].strip()
    enc_flag = long(enc_flag)
    print 'enc_flag:\n',enc_flag,'\n'

    s.send('4\n')
    pk = read_until(f,'L)')[:-1]
    pk = pk[pk.find(' (')+2:]
    line = map(long,pk.split(','))
    e = line[0]
    n = line[1]
    print 'e:\n',e,'\n'
    print 'n:\n',n,'\n'
# ============= command 1 get long(2) enc text ========#
    s.send('1\n')
    t = read_until(f,'.')
    print t
    s.send(l2b(2)+'\n')
    enc_two = read_until(f,'-').strip()
    enc_two = enc_two[enc_two.find(':')+1:-1]
    # print enc_two
    enc_two = long(enc_two)
    print 'enc_two:\n',enc_two,'\n'

# ============= Homomorphic cal =============#
# left shift and make it back by dividing 2.
    ans = ''
    # tmp1 = c1
    # tmp2 = c2
    tmp = enc_flag
    space = [0,n]
    # while True:
    #     print space[0]
    #     print space[1]
    #     if space[1] - space[0] == 0:
    #         print space[0]
    #         break
        # tmp1 = (tmp1*c1_2)%p
        # print tmp1
    tmp = (tmp*enc_two)%n
        # print tmp2
    s.send('2\n')
    t = read_until(f,'.')
    s.send(str(tmp)+'\n')
        # s.send(str(tmp2)+'\n')
    t = read_until(f,'-').strip()
    print t
    t = t[t.find(':')+1:-2].strip()
    print t
    b = l2b(long(t)/2)
    print b




# 1822151645672672111153904708950499107584117927558981259121239497850491645979402817333613650806522
# m1z0r3{I_love_Amazon:)#PEHJ-GZAWYX-HWFC}
if __name__ == '__main__':
    main()
