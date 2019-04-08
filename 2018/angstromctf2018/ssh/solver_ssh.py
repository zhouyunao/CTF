'''
00 00 00 07             The length in bytes of the next field
73 73 68 2d 72 73 61    The key type (ASCII encoding of "ssh-rsa")
00 00 00 03             The length in bytes of the public exponent
01 00 01                The public exponent (usually 65537, as here)
00 00 01 01             The length in bytes of the modulus (here, 257)
00 be 5d...             The modulus
'''
import base64
pk = 'AAAAB3NzaC1yc2EAAAADAQABAAABAQC+XZWLCbIpHPC9NlEckVXiKfiujcyu4VUslmm4G1MqNjtPNHaUEoZ8z5LLQK3e9SAKBdze8JyNowmC+lQT2VL059s9pzlRn6t31XTeUjZslgOs6IfAy/MsUkfOwUIo6KcqpSVnmeVMQPOiLUZCza9eDdB3MxFY59hNuodW1TGku00ro+ecKZcvJ+uNC/nfgeLpzaI7Dd6tI8AKrr+g9Tgyd6Ihd3KanLXuWMRwGbbLMi1/uaQd86LVYt/SAvkGO15eUELP723c/kEjKGfhwSKo3MGM5R77uMxfm8DzKW8QkcowEO2FEnPUykBnV1PaiWrl/PoBWTp8hNUYxQPAruWB'

m = base64.b64decode(pk)[22:]
m = int(m.encode('hex'),16)

# m = 24031426009258585415105324998970701655451460140660105245278171650878655493832570145520528674334486553204442446050601099312855866652174529838264749199630546148628121934849433734634042641132125007923761347962489974645002007692970466377879714666376153284839287915500514317384370204031902874952028757660051907008749997171513281852774870171717680368772057416440542176768196388565781131705261355090923059616730128088291078728643698870108958810166348296696671079733506691833466453747784418214869999275238860856569886383373280256273665811649081849561360513128165462438255912304945446909477593597880634673262567888241113884033L

e = 65537

'''
echo -n "YC2/ZTbmSZFL9t5Em+ic2ayw0nNUSI6XO7+3tcT9TABzh94t9YLhiDcCgYEA0LFZOUTgvmnWAkwGSo/6huQOu/7VmsM7OBdFntgotOJXALXFqCeT2PMXyWVc9/6ObUZjz9LQUlT6mnzYwFrX4mPPOTY5nvCyjepQlSDA7w49yaRhXKCFRHmEieeFJqzrZoQG" | base64 -d | hd
00000000  60 2d bf 65 36 e6 49 91  4b f6 de 44 9b e8 9c d9  |`-.e6.I.K..D....|
00000010  ac b0 d2 73 54 48 8e 97  3b bf b7 b5 c4 fd 4c 00  |...sTH..;.....L.|
00000020  73 87 de 2d f5 82 e1 88  37 02 81 81 00 d0 b1 59  |s..-....7......Y|
00000030  39 44 e0 be 69 d6 02 4c  06 4a 8f fa 86 e4 0e bb  |9D..i..L.J......|
00000040  fe d5 9a c3 3b 38 17 45  9e d8 28 b4 e2 57 00 b5  |....;8.E..(..W..|
00000050  c5 a8 27 93 d8 f3 17 c9  65 5c f7 fe 8e 6d 46 63  |..'.....e\...mFc|
00000060  cf d2 d0 52 54 fa 9a 7c  d8 c0 5a d7 e2 63 cf 39  |...RT..|..Z..c.9|
00000070  36 39 9e f0 b2 8d ea 50  95 20 c0 ef 0e 3d c9 a4  |69.....P. ...=..|
00000080  61 5c a0 85 44 79 84 89  e7 85 26 ac eb 66 84 06  |a\..Dy....&..f..|
00000090

n => marker:02 82 0, size : 101(bit 257)
e => marker:02 , size : 03
d => marker:02 82 0, size : 100 (bit 256)
p => marker:02 81 , size : 81 (bit 129)
q => marker:02 81 , size : 81 (bit 129)
exp1 => marker:02 81 , size : 81 (bit 129)
exp2 => marker:02 81 , size : 81 (bit 129)
coef => marker:02 81 , size : 80 (bit 128)

'''
p_low = int('0x602dbf6536e649914bf6de449be89cd9acb0d27354488e973bbfb7b5c4fd4c007387de2df582e18837',16)
q_high = 0xd0b1593944e0be69d6024c064a8ffa86e40ebbfed59ac33b3817459ed828b4e25700b5c5a82793d8f317c9655cf7fe8e6d4663cfd2d05254fa9a7cd8c05ad7e263cf3936399ef0b28dea509520c0ef0e3dc9a4615ca08544798489e78526aceb668406


import time

debug = True

# display matrix picture with 0 and X
def matrix_overview(BB, bound):
    for ii in range(BB.dimensions()[0]):
        a = ('%02d ' % ii)
        for jj in range(BB.dimensions()[1]):
            a += '0' if BB[ii,jj] == 0 else 'X'
            a += ' '
        if BB[ii, ii] >= bound:
            a += '~'
        print a

def coppersmith_howgrave_univariate(pol, modulus, beta, mm, tt, XX):
    """
    Coppersmith revisited by Howgrave-Graham

    finds a solution if:
    * b|modulus, b >= modulus^beta , 0 < beta <= 1
    * |x| < XX
    """
    #
    # init
    #
    dd = pol.degree()
    nn = dd * mm + tt

    #
    # checks
    #
    if not 0 < beta <= 1:
        raise ValueError("beta should belongs in (0, 1]")

    if not pol.is_monic():
        raise ArithmeticError("Polynomial must be monic.")

    #
    # calculate bounds and display them
    #
    """
    * we want to find g(x) such that ||g(xX)|| <= b^m / sqrt(n)
    * we know LLL will give us a short vector v such that:
    ||v|| <= 2^((n - 1)/4) * det(L)^(1/n)
    * we will use that vector as a coefficient vector for our g(x)

    * so we want to satisfy:
    2^((n - 1)/4) * det(L)^(1/n) < N^(beta*m) / sqrt(n)

    so we can obtain ||v|| < N^(beta*m) / sqrt(n) <= b^m / sqrt(n)
    (it's important to use N because we might not know b)
    """
    if debug:
        # t optimized?
        print "\n# Optimized t?\n"
        print "we want X^(n-1) < N^(beta*m) so that each vector is helpful"
        cond1 = RR(XX^(nn-1))
        print "* X^(n-1) = ", cond1
        cond2 = pow(modulus, beta*mm)
        print "* N^(beta*m) = ", cond2
        print "* X^(n-1) < N^(beta*m) \n-> GOOD" if cond1 < cond2 else "* X^(n-1) >= N^(beta*m) \n-> NOT GOOD"

        # bound for X
        print "\n# X bound respected?\n"
        print "we want X <= N^(((2*beta*m)/(n-1)) - ((delta*m*(m+1))/(n*(n-1)))) / 2 = M"
        print "* X =", XX
        cond2 = RR(modulus^(((2*beta*mm)/(nn-1)) - ((dd*mm*(mm+1))/(nn*(nn-1)))) / 2)
        print "* M =", cond2
        print "* X <= M \n-> GOOD" if XX <= cond2 else "* X > M \n-> NOT GOOD"

        # solution possible?
        print "\n# Solutions possible?\n"
        detL = RR(modulus^(dd * mm * (mm + 1) / 2) * XX^(nn * (nn - 1) / 2))
        print "we can find a solution if 2^((n - 1)/4) * det(L)^(1/n) < N^(beta*m) / sqrt(n)"
        cond1 = RR(2^((nn - 1)/4) * detL^(1/nn))
        print "* 2^((n - 1)/4) * det(L)^(1/n) = ", cond1
        cond2 = RR(modulus^(beta*mm) / sqrt(nn))
        print "* N^(beta*m) / sqrt(n) = ", cond2
        print "* 2^((n - 1)/4) * det(L)^(1/n) < N^(beta*m) / sqrt(n) \n-> SOLUTION WILL BE FOUND" if cond1 < cond2 else "* 2^((n - 1)/4) * det(L)^(1/n) >= N^(beta*m) / sqroot(n) \n-> NO SOLUTIONS MIGHT BE FOUND (but we never know)"

        # warning about X
        print "\n# Note that no solutions will be found _for sure_ if you don't respect:\n* |root| < X \n* b >= modulus^beta\n"

    #
    # Coppersmith revisited algo for univariate
    #

    # change ring of pol and x
    polZ = pol.change_ring(ZZ)
    x = polZ.parent().gen()

    # compute polynomials
    gg = []
    for ii in range(mm):
        for jj in range(dd):
            gg.append((x * XX)**jj * modulus**(mm - ii) * polZ(x * XX)**ii)
    for ii in range(tt):
        gg.append((x * XX)**ii * polZ(x * XX)**mm)

    # construct lattice B
    BB = Matrix(ZZ, nn)

    for ii in range(nn):
        for jj in range(ii+1):
            BB[ii, jj] = gg[ii][jj]

    # display basis matrix
    if debug:
        matrix_overview(BB, modulus^mm)

    # LLL
    BB = BB.LLL()

    # transform shortest vector in polynomial
    new_pol = 0
    for ii in range(nn):
        new_pol += x**ii * BB[0, ii] / XX**ii

    # factor polynomial
    potential_roots = new_pol.roots()
    print "potential roots:", potential_roots

    # test roots
    roots = []
    for root in potential_roots:
        if root[0].is_integer():
            result = polZ(ZZ(root[0]))
            if gcd(modulus, result) >= modulus^beta:
                roots.append(ZZ(root[0]))

    #
    return roots

############################################
# Test on Stereotyped Messages
##########################################

print "//////////////////////////////////"
print "// TEST 1"
print "////////////////////////////////"

# RSA gen options (for the demo)
length_N = 1024  # size of the modulus
Kbits = 200      # size of the root
e = 3

# RSA gen (for the demo)
p = next_prime(2^int(round(length_N/2)))
q = next_prime(p)
N = p*q
ZmodN = Zmod(N);

# Create problem (for the demo)
K = ZZ.random_element(0, 2^Kbits)
Kdigits = K.digits(2)
M = [0]*Kbits + [1]*(length_N-Kbits);
for i in range(len(Kdigits)):
    M[i] = Kdigits[i]
M = ZZ(M, 2)
C = ZmodN(M)^e

# Problem to equation (default)
P.<x> = PolynomialRing(ZmodN) #, implementation='NTL')
pol = (2^length_N - 2^Kbits + x)^e - C
dd = pol.degree()

# Tweak those
beta = 1                                # b = N
epsilon = beta / 7                      # <= beta / 7
mm = ceil(beta**2 / (dd * epsilon))     # optimized value
tt = floor(dd * mm * ((1/beta) - 1))    # optimized value
XX = ceil(N**((beta**2/dd) - epsilon))  # optimized value

# Coppersmith
start_time = time.time()
roots = coppersmith_howgrave_univariate(pol, N, beta, mm, tt, XX)

# output
print "\n# Solutions"
print "we want to find:",str(K)
print "we found:", str(roots)
print("in: %s seconds " % (time.time() - start_time))
print "\n"

############################################
# Test on Factoring with High Bits Known
##########################################
print "//////////////////////////////////"
print "// TEST 2"
print "////////////////////////////////"

N = 24031426009258585415105324998970701655451460140660105245278171650878655493832570145520528674334486553204442446050601099312855866652174529838264749199630546148628121934849433734634042641132125007923761347962489974645002007692970466377879714666376153284839287915500514317384370204031902874952028757660051907008749997171513281852774870171717680368772057416440542176768196388565781131705261355090923059616730128088291078728643698870108958810166348296696671079733506691833466453747784418214869999275238860856569886383373280256273665811649081849561360513128165462438255912304945446909477593597880634673262567888241113884033L
# qbar is q + [hidden_size_random]
qbar = 146549045227354172989110651205310632574067392372993711861623526130946979713469625772410411197033006823693645223316947254702263484103463390279967082549781844195965622071604103417650285219901124684816890970225510506869249766243257198851929423415614722596274340364744833427253274910457484375928631423371701125119L

F.<x> = PolynomialRing(Zmod(N), implementation='NTL');
pol = x - qbar
dd = pol.degree()

# PLAY WITH THOSE:
#------------------------------------------------------------------
# 今回はここ！！！
# q >= N^beta
beta = 0.3                            # we should have q >= N^beta
epsilon = beta / 7                     # <= beta/7
mm = ceil(beta**2 / (dd * epsilon))    # optimized
tt = floor(dd * mm * ((1/beta) - 1))   # optimized
XX = ceil(N**((beta**2/dd) - epsilon)) # we should have |diff| < X

# Coppersmith
start_time = time.time()
roots = coppersmith_howgrave_univariate(pol, N, beta, mm, tt, XX)

# output
print "\n# Solutions"
print "we found:", roots
print("in: %s seconds " % (time.time() - start_time))

# >>> q = qbar-1424632288941771831337603800308463796316066632150831619174778883066872L
# >>> q
# 146549045227354172989110651205310632574067392372993711861623526130946979713469625772410411197033006823693645223316947254702263484103463390279967082549781844195965622071604103417650285219901124684816890970225510506869249766243257198851929421990982433654502509027141033118789478594390852225097012248592818058247L
# >>> N%q
# 0L
# >>> p = N/q
# >>> p
# 163982139712862418555526520701188853132435025142588334581109287244065993155706892302449577647543501705795708316995057467949529976798218410513821698432879399377481736303821213515873396833696040164615779257072417113571942677691455176550027493593024586313878742269786944829130979576180492741390980797445630429239L
# Now, we have both p and q. All we need to do is combine these into a DER file. Let's use rsatool to do this.
# id01@universeshaper:/volatile/downloads/rsatool-master$ python2 rsatool.py -e 65537 -p 16398213971286241... snip ...97445630429239 -q 14654904522735417298911... snip ...97012248592818058247 -f PEM -o id_rsa
# Using (p, q) to initialise RSA instance
#
# n =
# be5d958b09b2291cf0bd36511c9155e229f8ae8dccaee1552c9669b81b532a363b4f34769412867c
# cf92cb40addef5200a05dcdef09c8da30982fa5413d952f4e7db3da739519fab77d574de52366c96
# 03ace887c0cbf32c5247cec14228e8a72aa5256799e54c40f3a22d4642cdaf5e0dd077331158e7d8
# 4dba8756d531a4bb4d2ba3e79c29972f27eb8d0bf9df81e2e9cda23b0ddead23c00aaebfa0f53832
# 77a22177729a9cb5ee58c47019b6cb322d7fb9a41df3a2d562dfd202f9063b5e5e5042cfef6ddcfe
# 41232867e1c122a8dcc18ce51efbb8cc5f9bc0f3296f1091ca3010ed851273d4ca40675753da896a
# e5fcfa01593a7c84d518c503c0aee581
#
# e = 65537 (0x10001)
#
# d =
# 620075bb457b95d4d34ee586ae6957c87e090b7beeb2dd486712ec4c1ead1adf1e7b712bd6a10ee1
# 744f431a0228f512d076223617b2d0ebed3aa3bae3190faf0b2a003c75b2c2bb988ea882c7da42de
# 9bf7c922122c2cfd5542a87b2f9f35ded18281962b51338780a5ae1f2cc70d1023967db729a8167b
# 71d0a45a1c99590f3c4bfa59f6cb99808d1b8c4e5c0ca7feeec7f2c88f6cee0a343be1f1217c23c2
# ec0e779740374cffda319dc8797a0b010a58b0ad79e33adc3ca088dcbf4fdb68da954c49b3aa693f
# 0e0545d6845e3413d720a2df5c98158e4b45d2bd6e2ea08672db20644ea9aec7c192c1087b970564
# cd929d43e5ea32f1c1e19a266adb84ed
#
# p =
# e984b0820151d7ed6a86569073ea12e64d36fa33bc360082cd1e87ad0618f6dd6f0dbac674170c3d
# 11f1e8ea1208c48ee3c6313f7703138fc2d2dc8e94fdd4a427bd92a420de8a025d0423e80351acaa
# 2c92bfe5e11729602dbf6536e649914bf6de449be89cd9acb0d27354488e973bbfb7b5c4fd4c0073
# 87de2df582e18837
#
# q =
# d0b1593944e0be69d6024c064a8ffa86e40ebbfed59ac33b3817459ed828b4e25700b5c5a82793d8
# f317c9655cf7fe8e6d4663cfd2d05254fa9a7cd8c05ad7e263cf3936399ef0b28dea509520c0ef0e
# 3dc9a4615ca08544798489e78526aceb668406cb284ebe0ee0120defe7405ffe7d76fb6bb469183c
# b262822c9b6f3407
#
# Saving PEM as id_rsa
