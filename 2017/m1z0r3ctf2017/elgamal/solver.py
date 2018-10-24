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


remotehost = "13.113.218.1"
# remotehost = "192.168.0.4"
remoteport = 12345
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
    enc_flag = read_until(f,')').strip()
    enc_flag = enc_flag[enc_flag.find('(')+1:-1]
    c1,c2 = map(long,enc_flag.split(','))
    print 'c1:\n',c1,'\n'
    print 'c2:\n',c2,'\n'

    s.send('4\n')
    pk = read_until(f,'L)')[:-1]
    pk = pk[pk.find(' (')+2:]
    line = map(long,pk.split(','))
    y = line[0]
    g = line[1]
    p = line[2]
    print 'y:\n',y,'\n'
    print 'g:\n',g,'\n'
    print 'p:\n',p,'\n'
# ============= command 1 get long(2) enc text ========#
    s.send('1\n')
    s.send(l2b(2)+'\n')
    enc_two = read_until(f,')')
    enc_two = enc_two[enc_two.find('(')+1:-1]
    print enc_two
    line = map(long,enc_two.split(','))
    c1_2 = line[0]
    c2_2 = line[1]
    print 'c1_2:\n',c1_2,'\n'
    print 'c2_2:\n',c2_2,'\n'

# ============= Homomorphic cal =============#
    ans = ''
    tmp1 = c1
    tmp2 = c2
    space = [0,p]
    while True:
        print space[0]
        print space[1]
        if space[1] - space[0] == 0:
            print space[0]
            break
        tmp1 = (tmp1*c1_2)%p
        # print tmp1
        tmp2 = (tmp2*c2_2)%p
        # print tmp2
        s.send('2\n')
        t = read_until(f,'c1:')
        s.send(str(tmp1)+'\n')
        s.send(str(tmp2)+'\n')
        t = read_until(f,'\n').strip()
        # print t
        t = t[t.find(':')+1:].strip()
        # print t
        if '0' in t:
            space[1] = (space[0] + space[1])/2
        if '1' in t:
            space[0] = (space[0] + space[1])/2




    # 69738345988067693181314793186309978610630742549490905494208294511042643521281937979300103764610521451627246631677319339182822908610794392454479662058908169381185634181102047282880328141368645925991377533350995542987546641350646000961945495137116228421431107018007766909403934581044144731898196412
    # m1z0r3{ElGamal_1s_h0m0m0rph1c_3ncrypt10n!!}
    # \nService Problem(It have a no connection with the score.)->nc 13.113.218.1 54321\xbc'
if __name__ == '__main__':
    main()
