# coding: utf-8
f = open('enc_pubkey.txt')
for r in f:
    exec(r)

def continued_fraction(p,q):
    result = []
    t = 0
    while q != 1:
        t = q/p
        s = q % p
        q = p
        p = s
        result.append(t)
    return result

def shiki(n,b0,b1,alist):
    idx = 0
    r = 0
    if n == 0:
        return b0
    if n == 1:
        return b1
    else:
        while idx+2 <= n:
            r = b0+alist[idx+1]*b1
            b0 = b1
            b1 = r
            idx+=1
        return r


wiener_attack(e,n)
def wiener_attack(e,N):
    clist = continued_fraction(N,e)
    l = len(clist)
    for n in range(1,l):
        k = shiki(n,1,clist[0],clist)
        d = shiki(n,0,1,clist)
        if k == 0:
            continue
        if (e*d-1)%k == 0:
            print 'k={}\nd={}'.format(k,d)



def ex_shiki(n,b0,b1,s,r,alist):
    idx = 0
    result = 0
    if n == 0:
        return b0
    if n == 1:
        return b1
    else:
        while idx+2 <= n:
            result = r*b0+s*b1
            b0 = b1
            b1 = result
            idx+=1
        return result


ex_wiener_attack(e,n)
def ex_wiener_attack(e,N):
    clist = continued_fraction(N,e)
    l = len(clist)
    dlist = list()
    for n in range(1,l):
        k = shiki(n,1,clist[0],clist)
        d = shiki(n,0,1,clist)
        print (k,d)
        dlist.append(d)
    print '[+] There are {}'.format(len(dlist))
    for n in range(len(dlist)):
        print '[+] {}/{}'.format(n,len(dlist))
        for s in range(10):
            for r in range(10):
                d = ex_shiki(n,dlist[0],dlist[1],s,r,dlist)
                if pow(5,e*d,N) == 5:
                    print 'd={}'.format(d)




ex_wiener_attack(e,n)
def ex_wiener_attack(e,N):
    clist = continued_fraction(N,e)
    l = len(clist)
    dlist = list()
    for n in range(1,l):
        k = shiki(n,1,clist[0],clist)
        d = shiki(n,0,1,clist)
        dlist.append(d)
    print '[+] There are {}'.format(len(dlist))
    for n in range(len(dlist)):
        print '[+] {}/{}'.format(n,len(dlist))
        for s in range(10):
            for r in range(10):
                d = s * dlist[n-1] + r * dlist[n-2]
                if pow(5,e*d,N) == 5:
                    print 'd={}'.format(d)



ex_wiener_attack(e,n)
exec('d=100556095937036905102538523179832446199526507742826168666218687736467897968451')
c
c1,c2 = c
k = pow(c1,d,n)
k
a
from Crypto.Util.number import long_to_bytes,bytes_to_long
from Crypto.Util.number import inverse
w = inverse(k,a)
w
K = pow(g,k,a)
long_to_bytes((c2*inverse(K,a))%a)
