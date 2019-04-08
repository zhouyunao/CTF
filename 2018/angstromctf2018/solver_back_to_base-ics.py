flag_p1 = ''.join([chr(int(b[i:i+8],2)) for i in range(0,len(b)+1-8,8)])
# actf{0ne_tw0_f0
flag_p2 = ''.join([chr(int(i,8)) for i in p2.split(' ')])
# ur_eight_sixt33
flag_p3 = ''.join([chr(int(p3[i:i+2],16)) for i in range(0,len(p3)+1-2)])
# n_th1rtytw0_s1x
flag_p4 = base64.b64decode('dHlmMHVyX25vX20wcmV9')
# tyf0ur_no_m0re}
