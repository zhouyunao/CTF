IV = '0x61'
msg = 'fbf9eefce1f2f5eaffc5e3f5efc5efe9fffec5fbc5e9f9e8f3eaeee7'

''.join([chr(int(IV,16)^int(msg[i:i+2],16)) for i in range(0,len(msg)+1-2,2)])
