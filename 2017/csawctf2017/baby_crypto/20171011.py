import socket, struct, telnetlib

# --- common funcs ---
def sock(remoteip, remoteport):
# --- meke the socket ---
# --- AF_INET->internet socket
# --- SOCK_STREAM->TCP BTW SOCK_DGRAM->UDP
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((remoteip, remoteport))
    return s, s.makefile('rw', bufsize=0)

def read_until(f, delim='\n'):
    data = ''
    while not data.endswith(delim):
        data += f.read(1)
    return data

remotehost = "crypto.chal.csaw.io"
remoteport = 1578
s,f = sock(remotehost,remoteport)
def get_cookie(username):
    read_until(f,"whitespace):")
    s.send(username+"\n")
    read_until(f,"is: ")
    return read_until(f).strip()

def main():


    flag = ""
    for i in range(31,-1,-1):
        for j in range(32,127):
            print "test:",chr(j)
            if get_cookie("a"*i)[:64] == get_cookie("a"*i+flag+chr(j))[:64]:
                print "bingo-->",chr(j)
                flag += chr(j)
                break

    print flag
if __name__=="__main__":
    main()
