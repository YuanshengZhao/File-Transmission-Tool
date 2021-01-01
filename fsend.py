import socket
import os
import sys

port = 27010

maxrecv=len(sys.argv)
if(maxrecv<2):
    print("No file given!\nUsage: fsend.py file-name address")
    sys.exit()
else:
    fnm=bytearray(sys.argv[1],'utf-8')



s=socket.socket()


if(maxrecv>2):
    print("Connecting...")
    s.connect((sys.argv[2], port))
    c=s
    print("Connection successful: ")
else:
    print("Server mode.")
    print(socket.gethostbyname(socket.getfqdn()))
    s.bind(('', 27010))
    s.listen()
    c, addr = s.accept()
    print("Connected: ", addr)

fp=open(sys.argv[1],"rb")
maxrecv=50000

fsize=os.path.getsize(fnm)
msg=b'f'+(fsize.to_bytes(8,byteorder='big'))+b'recv-'+fnm+b'\n'
nhdr=len(msg)

nhsnd=c.send(msg+fp.read(maxrecv-nhdr))-nhdr
while(nhsnd<fsize):
    nhsnd+=c.send(fp.read(maxrecv))
    print(str(nhsnd)+"\r",end="")

fp.close()
nrtn=int.from_bytes(c.recv(8),byteorder='big')

if(c!=s):
    s.shutdown(socket.SHUT_RDWR)
    s.close()

c.shutdown(socket.SHUT_RDWR)
c.close()

print("File size =",fsize,"\nSent =",nrtn,"\nDone!")
