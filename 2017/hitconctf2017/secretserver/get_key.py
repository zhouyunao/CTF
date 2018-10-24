import os, base64, time, random, string
from Crypto.Cipher import AES
from Crypto.Hash import *
import socket,itertools
import time
import struct
encrypted = 'MmpwbUxvU3NPbFFycXlxRWxGsUl5HJ4+v+AmPC0DIHs='

asciimap = string.ascii_letters+string.digits
def sxor(s1,s2):
    return ''.join(chr(ord(a) ^ ord(b)) for a,b in zip(s1,s2))

def part_sxor(s1,s2):
    if len(s1) > len(s2):
        return sxor(s1,s2)+s1[len(s2):]
    elif len(s1) < len(s2):
        return sxor(s1,s2)+s2[len(s1):]
    else:
        return sxor(s1,s2)

def read_until(f, delim='\n'):
    data = ''
    while not data.endswith(delim):
        data += f.read(1)
    return data

def passdone(f,delim='\n'):
    data = ''
    while not data.endswith(delim) or data[-2] =='!':
        data += f.read(1)
    return data

def exchange(plain,command,iv):
    iv_new = sxor(iv,sxor(plain,command))
    return iv_new

def sock(remoteip, remoteport):
# --- meke the socket ---
# --- AF_INET->internet socket
# --- SOCK_STREAM->TCP BTW SOCK_DGRAM->UDP
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((remoteip, remoteport))
    return s, s.makefile('rw', bufsize=0)


def test(proof4after,digest):
    flag = 0
    for c0 in asciimap:
        for c1 in asciimap:
            for c2 in asciimap:
                for c3 in asciimap:
                    # print c0+c1+c2+c3
                    if SHA256.new(c0+c1+c2+c3+proof4after).hexdigest() == digest:
                        print 'Bingo'
                        return c0+c1+c2+c3

# G = 'get-flag\x08\x08\x08\x08\x08\x08\x08\x08'
# W = 'Welcome!!\x07\x07\x07\x07\x07\x07\x07'
# iv = '2jpmLoSsOlQrqyqE'
# encrypt :
#          C = E(W ^ iv)
# send b64encode(iv + C) > msg
# recv msg
# iv = b64decode(msg)[:16]
# C = b64decode(msg)[16:]
# decrypt :
#          D = iv ^ D(C)
# M = W ^ iv
# let Welcome! become get-flag


# proof_of_work
# for x in itertools.product(s,repeat=4):
#     "".join(x)

remotehost = "52.193.157.19"
remoteport = 9999
s,f = sock(remotehost,remoteport)

start_text = read_until(f,':')
from4 = start_text[12:28]
sha  = start_text[33:97]
print start_text
# print from4
# print sha

# time.sleep(10)
first4 = test(from4,sha)
s.send(first4+'\n')

X = '\x02jh#EnW5fc^}~v~J'

plain = 'Welcome!!'+'\x07'*7
command_flag = 'get-flag'+'\x08'*8

iv_new = ''
iv = '2jpmLoSsOlQrqyqE'


# xrange is python 2
print '----------welcome------------'
# print f

enc_wel = passdone(f,'\n')[6:-1]
print enc_wel
enc_wel = base64.b64decode(enc_wel)[16:]
# print enc_wel
print '-----------get-flag------------'
new_iv = exchange(plain,command_flag,iv)

s.send(base64.b64encode(new_iv+enc_wel)+'\n')
enc_flag = read_until(f,'\n')[:-1]

print enc_flag

enc_flag = base64.b64decode(enc_flag)[16:]

# print enc_flag

print '--------get-md5----------'

iv_md5 = exchange(plain,'get-md5'+'\x09'*9,iv)
s.send(base64.b64encode(iv_md5+enc_wel)+'\n')

enc_md5 = read_until(f,'\n')[:-1]
print enc_md5

# enc_md5 = base64.b64decode(enc_md5)[16:]

print '--------get-num---------'
x=0
for i in xrange(256):
    iv_hit_md5 = exchange('hitcon{'+'\x09'*9,'get-md5'+'\x09'*9,iv)
    new_enc_flag = enc_flag[:31]+chr(i)+enc_flag[32:]
    # print i
    s.send(base64.b64encode(iv_hit_md5+new_enc_flag)+'\n')
    recv = read_until(f,'\n')[:-1]
    # print recv
    if recv == enc_md5:
        print 'BINGO'
        # print i
        x=i
        break
print 'padding length:'
print ord(sxor(sxor(chr(x),chr(41)),enc_flag[31]))
print '----------flag bf--------------'


# block 1
block_1 = ''
def block1(ans,x):

    for i in xrange(9):
        mid47 =sxor( chr(x),chr(41) )
        new_f31 = sxor(mid47,chr(41-i-1))
        tes_enc_flag  = enc_flag[:31]+new_f31+enc_flag[32:]
        iv_1 = part_sxor('hitcon{',part_sxor('get-md5',iv))
        # print iv_1
        s.send(base64.b64encode(iv_1+tes_enc_flag)+'\n')
        recv_sample = read_until(f,'\n')[:-1]
        # print recv_sample
        sample = base64.b64decode(recv_sample)[16:]
        for j in xrange(256):
            MD5_x = MD5.new(ans+chr(j)).digest()[:16]
            iv_test =part_sxor(part_sxor(MD5_x,'get-flag'),iv)
            s.send(base64.b64encode(iv_test+sample)+'\n')
            test_recv = read_until(f,'\n')[:-1]
            if len(test_recv) > 64:
                # print chr(j)
                ans += chr(j)
                break
    return ans
block_1 = block1(block_1,x)
print block_1
block_2 = ''
def block2(block_1,ans,x):
    for i in xrange(16):
        mid53 = sxor(chr(x),chr(41))
        new_f47 = sxor(mid53,chr(48-i-1))
        test_enc_flag = enc_flag[:32]+enc_flag[16:31]+new_f47+enc_flag[32:]
        iv_2 = part_sxor('hitcon{',part_sxor('get-md5',iv))
        s.send(base64.b64encode(iv_2+test_enc_flag)+'\n')
        recv_sample = read_until(f,'\n')[:-1]
        # print recv_sample
        sample = base64.b64decode(recv_sample)[16:]

        for j in xrange(256):
            MD5_x = MD5.new(block_1+ans+chr(j)).digest()[:16]
            iv_test = part_sxor(part_sxor(MD5_x,'get-flag'),iv)
            s.send(base64.b64encode(iv_test+sample)+'\n')
            test_recv = read_until(f,'\n')[:-1]
            if len(test_recv) > 64:
                # print chr(j)
                ans += chr(j)
                break
    return ans
block_2 = block2(block_1,block_2,x)
print block_2

print 'hitcon{'+block_1+block_2
# msg =base64.b64encode(new_iv+enc_wel)
# print msg

# enc_flag = raw_input('input encrypted flag')
# enc_flag = base64.b64decode(enc_flag)[16:]
#
# # flag:   hitcon{xxxxxxxxxxxxxxxx}
#
# # hitcon{ --> get-flag
# new_iv = exchange(,command_flag)
